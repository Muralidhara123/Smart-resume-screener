from backend.nlp_engine import calculate_similarity

jd = "Java"
resume = "I am a Java Developer"
score = calculate_similarity(resume, jd)
print(f"JD: {jd}")
print(f"Resume: {resume}")
print(f"Score: {score}")

jd2 = "Python Machine Learning"
resume2 = "I know Python and Machine Learning"
score2 = calculate_similarity(resume2, jd2)
print(f"JD: {jd2}")
print(f"Resume: {resume2}")
print(f"Score: {score2}")
