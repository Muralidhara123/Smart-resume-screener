from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from typing import List
sys.path.append(os.getcwd())

from backend.nlp_engine import (
    extract_text_from_pdf, 
    calculate_similarity, 
    get_missing_keywords, 
    predict_category,
    extract_degree,
    extract_experience_years,
    categorize_skills,
    calculate_match_strength
)
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/score")
async def score_resumes(resumes: List[UploadFile] = File(...), jd_text: str = Form(...)):
    """
    Endpoint to score multiple resumes against a job description.
    Returns enhanced analysis with experience, skills, and match strength.
    """
    results = []
    
    for resume in resumes:
        try:
            file_bytes = await resume.read()
            resume_text = extract_text_from_pdf(file_bytes)
            
            if not resume_text:
                results.append({
                    "filename": resume.filename,
                    "error": "Could not extract text from PDF"
                })
                continue
            
            # Calculate all metrics
            score = calculate_similarity(resume_text, jd_text)
            missing_keywords = get_missing_keywords(resume_text, jd_text)
            category = predict_category(resume_text)
            degree = extract_degree(resume_text)
            experience = extract_experience_years(resume_text)
            skills = categorize_skills(resume_text)
            match_strength = calculate_match_strength(score)
            
            results.append({
                "filename": resume.filename,
                "score": score,
                "missing_keywords": missing_keywords,
                "category": category,
                "degree": degree,
                "experience": experience,
                "skills": skills,
                "match_strength": match_strength,
                "resume_text_preview": resume_text[:100] + "..."
            })
            
        except Exception as e:
            results.append({
                "filename": resume.filename,
                "error": f"Error processing resume: {str(e)}"
            })
    
    return JSONResponse(content=results)

# Mount static files
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
