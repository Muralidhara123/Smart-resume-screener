from backend.nlp_engine import calculate_similarity, get_missing_keywords

jd = "Python Java SQL"
resume = "I have experience in Python, Java, and SQL."

score = calculate_similarity(resume, jd)
missing = get_missing_keywords(resume, jd)

print(f"JD: {jd}")
print(f"Resume: {resume}")
print(f"Score: {score}")
print(f"Missing: {missing}")

if not missing and score == 100.0:
    print("SUCCESS: No missing keywords and Score is 100%")
else:
    print("FAILURE: Logic mismatch")
