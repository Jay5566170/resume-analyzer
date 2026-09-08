
## 📄 README FOR RESUME ANALYZER

**Create `README.md` in your `resume-analyzer` folder:**

```markdown
# Resume Analyzer

An AI-powered web application that extracts structured data from resumes using **Google Gemini API**. Upload a PDF or TXT resume, and the AI extracts name, email, skills, experience, education, and summary.

---

## 🚀 Features

- ✅ **Upload Resume** — Support for PDF and TXT files
- ✅ **AI-Powered Extraction** — Uses Google Gemini API
- ✅ **Structured Data** — Name, email, skills, experience, education
- ✅ **Search** — Search by name, email, or skills
- ✅ **Delete** — Remove unwanted resumes
- ✅ **Beautiful UI** — Clean, responsive frontend
- ✅ **Live Deployment** — Hosted on Railway

---

## 🛠️ Tech Stack

| **Technology** | **Purpose** |
|----------------|-------------|
| **Backend** | FastAPI, Python, SQLite |
| **AI** | Google Gemini API |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Railway |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jay5566170/resume-analyzer.git
   cd resume-analyzer
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Create .env file:

env
GEMINI_API_KEY=your-api-key-here
DATABASE_URL=sqlite:///./resumes.db
Run the server:

bash
cd backend
python run.py
Open the frontend:

Open frontend/index.html in your browser

📊 API Endpoints
Method	Endpoint	Description
POST	/resumes/upload	Upload a resume
POST	/resumes/analyze/{id}	Analyze a resume with AI
GET	/resumes/	Get all resumes
GET	/resumes/{id}	Get one resume
DELETE	/resumes/{id}	Delete a resume
GET	/resumes/search/	Search resumes
🧠 How It Works
User uploads a resume (PDF or TXT)

PDF text is extracted using PyPDF2

Text is sent to Google Gemini API with a prompt

AI extracts structured data (name, email, skills, etc.)

Data is stored in the database

User can view, search, and delete resumes

📝 Example Response
json
{
  "name": "Mujahid Khan",
  "email": "shelimeli666@gmail.com",
  "skills": ["Python", "FastAPI", "SQL", "REST APIs"],
  "experience": ["Student Manager Project"],
  "education": ["BS Computer Science - COMSATS University"],
  "summary": "Computer Science graduate with Python and API development skills."
}
🔗 Links
GitHub: Jay5566170/resume-analyzer

Live Demo: Resume Analyzer

📄 License
This project is for learning purposes only.

text

---

## 📝 UPDATE REPOSITORY DESCRIPTIONS

### Student Manager
**Description:** A complete REST API for managing student records built with FastAPI and PostgreSQL. Demonstrates CRUD operations, SQLAlchemy ORM, and production-ready database integration.

### Resume Analyzer
**Description:** AI-powered resume analyzer that extracts structured data from PDF resumes using Google Gemini API. Built with FastAPI, SQLite, and a clean frontend.

---

## ✅ WHAT TO DO NOW

1. **Create `README.md`** in both project folders
2. **Update the repository descriptions** on GitHub
3. **Commit and push**

```powershell
# Student Manager
cd student-manager
git add README.md
git commit -m "Add professional README"
git push origin main

# Resume Analyzer
cd ../resume-analyzer
git add README.md
git commit -m "Add professional README"
git push origin main
