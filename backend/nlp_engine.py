import re
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io

def extract_text_from_pdf(file_bytes):
    """Extracts text from a PDF file stream."""
    try:
        text = extract_text(io.BytesIO(file_bytes))
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def clean_text(text):
    """Cleans text by removing special characters and extra spaces."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def get_top_keywords(text, top_n=20):
    """Extracts top N keywords from text using TF-IDF."""
    clean = clean_text(text)
    if not clean:
        return []
    
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        vectorizer.fit([clean])
        feature_names = vectorizer.get_feature_names_out()
        response = vectorizer.transform([clean])
        feature_array = response.toarray()[0]
        tfidf_sorting = feature_array.argsort()[::-1]
        
        # Return top_n keywords
        return [feature_names[i] for i in tfidf_sorting[:top_n]]
    except ValueError:
        return []

def calculate_similarity(resume_text, jd_text):
    """Calculates similarity using a hybrid of Cosine Similarity and Keyword Coverage."""
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)
    
    if not clean_resume or not clean_jd:
        return 0.0

    # 1. Cosine Similarity
    cosine_score = 0.0
    try:
        documents = [clean_resume, clean_jd]
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        cosine_score = round(similarity_matrix[0][0] * 100, 2)
    except Exception:
        cosine_score = 0.0

    # 2. Keyword Coverage Score (based on Top JD Keywords)
    coverage_score = 0.0
    try:
        jd_keywords = get_top_keywords(jd_text, top_n=20)
        if jd_keywords:
            resume_tokens = set(clean_resume.split())
            matched_count = sum(1 for kw in jd_keywords if kw in resume_tokens)
            coverage_score = round((matched_count / len(jd_keywords)) * 100, 2)
    except Exception:
        coverage_score = 0.0

    # Return the maximum of the two scores
    return max(cosine_score, coverage_score)

def get_missing_keywords(resume_text, jd_text, top_n=10):
    """Identifies keywords present in JD but missing in Resume."""
    clean_resume = clean_text(resume_text)
    
    jd_keywords = get_top_keywords(jd_text, top_n=20)
    resume_tokens = set(clean_resume.split())
    
    missing = [kw for kw in jd_keywords if kw not in resume_tokens]
    return missing[:top_n]

def predict_category(text):
    """Predicts the sector/category of the resume based on keywords."""
    text = clean_text(text)
    
    categories = {
        "IT / Tech": ["python", "java", "c++", "sql", "aws", "docker", "react", "node", "developer", "software", "engineer"],
        "Finance": ["finance", "accounting", "audit", "tax", "budget", "forecast", "reporting", "analyst", "excel"],
        "HR": ["recruitment", "human resources", "employee", "hiring", "onboarding", "training", "payroll"],
        "Marketing": ["marketing", "seo", "content", "social media", "campaign", "brand", "advertising"],
        "Sales": ["sales", "revenue", "account", "client", "negotiation", "crm", "target"]
    }
    
    scores = {cat: 0 for cat in categories}
    
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                scores[cat] += 1
                
    # Return category with max score, or "General" if no matches
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        return "General"
    return best_cat

def extract_degree(text):
    """Extracts the highest degree from resume text."""
    text_lower = text.lower()
    
    # Define degree patterns in order of priority (highest to lowest)
    degrees = {
        "PhD / Doctorate": ["phd", "ph.d", "doctorate", "doctoral"],
        "Master's": ["master", "mba", "m.tech", "m.sc", "m.s", "ms ", "mca", "m.a"],
        "Bachelor's": ["bachelor", "b.tech", "b.e", "b.sc", "b.s", "bs ", "bca", "b.a", "bba"],
        "Diploma": ["diploma", "associate"],
        "High School": ["high school", "12th", "intermediate", "senior secondary"]
    }
    
    # Check for degrees in priority order
    for degree, patterns in degrees.items():
        for pattern in patterns:
            if pattern in text_lower:
                return degree
    
    return "Not Specified"

def extract_experience_years(text):
    """Extracts years of experience from resume text."""
    text_lower = text.lower()
    
    # Pattern 1: "X years of experience" or "X+ years"
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*:?\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
    ]
    
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            years = int(match)
            if years > max_years and years < 50:  # Sanity check
                max_years = years
    
    if max_years > 0:
        return f"{max_years}+ years"
    
    # Check for fresher/entry level keywords
    fresher_keywords = ["fresher", "entry level", "recent graduate", "new graduate"]
    for keyword in fresher_keywords:
        if keyword in text_lower:
            return "Fresher"
    
    return "Not specified"

def categorize_skills(text):
    """Categorizes skills into technical and soft skills."""
    text_lower = text.lower()
    
    technical_keywords = [
        "python", "java", "javascript", "react", "angular", "node", "sql", "mongodb",
        "aws", "azure", "docker", "kubernetes", "git", "machine learning", "ai",
        "data science", "html", "css", "c++", "ruby", "php", "swift", "kotlin",
        "tensorflow", "pytorch", "django", "flask", "spring", "vue", "typescript"
    ]
    
    soft_keywords = [
        "leadership", "communication", "teamwork", "problem solving", "analytical",
        "creative", "adaptability", "time management", "critical thinking",
        "collaboration", "presentation", "negotiation", "management"
    ]
    
    found_technical = [skill for skill in technical_keywords if skill in text_lower]
    found_soft = [skill for skill in soft_keywords if skill in text_lower]
    
    return {
        "technical": found_technical[:8],  # Limit to top 8
        "soft": found_soft[:5]  # Limit to top 5
    }

def calculate_match_strength(score):
    """Calculates match strength category based on score."""
    if score >= 80:
        return "Excellent Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 40:
        return "Potential Match"
    else:
        return "Weak Match"
