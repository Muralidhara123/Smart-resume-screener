# Smart Resume Screener

An AI-powered resume screening application that intelligently analyzes and ranks candidates based on job descriptions.

## 🌟 Features

- **AI-Powered Analysis**: Advanced NLP-based resume scoring and ranking
- **Experience Detection**: Automatically extracts years of experience
- **Skills Categorization**: Separates technical and soft skills
- **Match Strength Indicators**: Clear visual indicators (Excellent/Good/Potential/Weak Match)
- **Interactive Analytics**: Beautiful charts for score distribution and degree breakdown
- **Modern UI**: Professional gradient design with smooth animations
- **Real-time Processing**: Fast analysis of multiple resumes simultaneously

## 🚀 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **scikit-learn** - ML algorithms for similarity calculation
- **PDFMiner** - PDF text extraction
- **TF-IDF** - Keyword extraction and analysis

### Frontend
- **HTML5/CSS3** - Modern web standards
- **JavaScript** - Dynamic interactions
- **Chart.js** - Interactive data visualizations
- **Gradient UI** - Premium design aesthetics

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Muralidhara123/Smart-resume-screener.git
cd Smart-resume-screener
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python backend/main.py
```

4. **Access the application**
```
http://localhost:8000
```

## 💡 How to Use

1. **Enter Job Description**: Paste the job requirements in the text area
2. **Upload Resumes**: Select one or multiple PDF resumes
3. **Analyze**: Click the analyze button to process
4. **Review Results**: View ranked candidates with detailed insights

## 📊 What It Analyzes

- **Match Score**: Overall compatibility percentage
- **Missing Keywords**: Skills gap analysis
- **Experience Level**: Years of experience or fresher status
- **Technical Skills**: Programming languages, frameworks, tools
- **Soft Skills**: Communication, leadership, teamwork
- **Education**: Degree level detection
- **Category**: Job role classification

## 🎨 Screenshots

The application features:
- Animated gradient backgrounds
- Interactive floating particles
- Smooth hover effects
- Professional candidate cards
- Color-coded skill badges
- Real-time analytics charts

## 🔧 Configuration

The application runs on port 8000 by default. You can modify this in `backend/main.py`:

```python
uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
```

## 📝 API Endpoints

### POST /api/score
Analyzes resumes against a job description.

**Request:**
- `resumes`: Multiple PDF files
- `jd_text`: Job description text

**Response:**
```json
[
  {
    "filename": "resume.pdf",
    "score": 85,
    "match_strength": "Excellent Match",
    "experience": "5+ years",
    "skills": {
      "technical": ["Python", "React", "SQL"],
      "soft": ["Leadership", "Communication"]
    },
    "missing_keywords": ["Docker", "AWS"],
    "category": "Software Development",
    "degree": "Bachelor's"
  }
]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Muralidhara123**

## 🙏 Acknowledgments

- Built with FastAPI and modern web technologies
- Powered by advanced NLP algorithms
- Designed for recruiters and HR professionals

---

**Note**: This application requires PDF resumes and works best with well-formatted documents.
