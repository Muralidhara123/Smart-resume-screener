import streamlit as st
import sys
import os

# Add the current directory to sys.path to allow imports from backend
sys.path.append(os.getcwd())

from backend.nlp_engine import extract_text_from_pdf, calculate_similarity, get_missing_keywords

# Page Config
st.set_page_config(page_title="Smart Resume Screener", page_icon="📄", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(75, 108, 183, 0.4);
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    h1 {
        background: -webkit-linear-gradient(#eee, #999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }
    h2, h3 {
        color: #e0e0e0 !important;
    }
    .metric-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #2e3344;
        text-align: center;
    }
    .highlight-good {
        color: #4caf50;
        font-weight: bold;
    }
    .highlight-missing {
        color: #ff5252;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 Smart Resume Screener")
st.markdown("### AI-Powered Resume Analysis & Scoring")
st.markdown("---")

# Layout: 2 Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the Job Description here...", height=300)

    analyze_btn = st.button("Analyze Resume")

with col2:
    st.subheader("📊 Analysis Results")
    
    if analyze_btn:
        if uploaded_file is not None and jd_text:
            with st.spinner("Analyzing..."):
                # Read PDF
                file_bytes = uploaded_file.read()
                resume_text = extract_text_from_pdf(file_bytes)
                
                if resume_text:
                    # Calculate Score
                    score = calculate_similarity(resume_text, jd_text)
                    missing_keywords = get_missing_keywords(resume_text, jd_text)
                    
                    # Display Score
                    st.markdown(f"""
                        <div class="metric-card">
                            <h2>Match Score</h2>
                            <h1 style="font-size: 4rem; margin: 0;">{score}%</h1>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 🔍 Insights")
                    
                    # Missing Keywords
                    if missing_keywords:
                        st.warning(f"⚠️ Missing Keywords: {', '.join(missing_keywords)}")
                    else:
                        st.success("✅ Great job! Your resume covers the top keywords.")
                        
                    # Resume Preview (Snippet)
                    with st.expander("View Extracted Resume Text"):
                        st.text(resume_text)
                        
                else:
                    st.error("Could not extract text from the PDF. Please try another file.")
        elif not uploaded_file:
            st.info("Please upload a resume to begin.")
        elif not jd_text:
            st.info("Please paste a job description.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Python & Streamlit")
