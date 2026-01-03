# GFGBQ — Team techno_guys

Repository for Team techno_guys — Vibe Coding Hackathon

## 📌 Problem Statement

**PS-12: AI for Grievance Redressal in Public Governance**

Government bodies receive thousands of citizen grievances daily related to infrastructure, sanitation, healthcare, public safety, utilities, and administrative delays. These grievances are often unstructured (free text, mixed languages) and manually processed, which slows resolution. The lack of intelligent prioritization and routing causes delayed resolution of critical issues, citizen dissatisfaction, and reduced transparency.

There is a need for an AI-powered system that can automatically analyze, classify, prioritize, and route grievances to enable faster, fairer, and more accountable governance.

## 🚀 Project Name

**SmartGov AI — Intelligent Grievance Redressal System**

## 👥 Team

**Team ByteQuest AI**

## 🌐 Deployed Link (optional)

`https://your-deployed-link.com`

## 🎥 2-Minute Demonstration Video (optional)

`https://your-demo-video-link.com`  
(YouTube unlisted / Google Drive)

## 📊 Presentation (optional)

`https://your-ppt-link.com`  
(Google Slides / Drive)

## 📖 Project Overview

SmartGov AI is an AI-driven grievance redressal platform that helps government bodies automatically understand, prioritize, and route citizen complaints using Natural Language Processing (NLP).

The system accepts free-text grievances, analyzes them using AI, classifies them into categories (e.g., sanitation, healthcare, infrastructure), determines priority based on urgency and severity, and routes them to the appropriate department. This reduces manual workload, speeds up resolution, and improves transparency and accountability.

## 🧠 Key Features

- Free-text grievance submission
- AI-based complaint classification (NLP)
- Priority detection (High / Medium / Low)
- Automatic department routing
- Admin dashboard for grievance monitoring
- Dataset-driven, scalable architecture

## 🛠️ Tech Stack

- Frontend: React.js, HTML, CSS, JavaScript  
- Backend: Streamlit (Python)  
- AI / ML: Python, Transformers / NLP models  
- Dataset: Structured grievance dataset (CSV)

## ⚙️ Setup and Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/smartgov-ai.git
cd smartgov-ai
```

1. Frontend (React)

```bash
cd frontend
npm install
npm start
```

The React app will run at: <http://localhost:3000>

1. Backend (Streamlit)

Create and activate a virtual environment (recommended)

- macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

- Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

- Windows (cmd.exe):

```cmd
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit backend:

```bash
streamlit run app.py
```

Backend will run at: <http://localhost:8501>

## ▶️ Usage

1. Open the React frontend in your browser (<http://localhost:3000>).  
2. Enter a grievance in free text (e.g., “Garbage not collected for 7 days”) and submit.  
3. The AI backend processes the text and:

- Classifies the grievance category
- Determines priority level
- Assigns the relevant department  

4. Admin dashboard displays processed grievances with status and history.

## 📸 Screenshots

- Citizen Grievance Submission Interface  
  `/screenshots/citizen_form.png`

- AI Classification & Priority Output  
  `/screenshots/ai_output.png`

- Admin Dashboard  
  `/screenshots/admin_dashboard.png`

(Add screenshots to the referenced paths)

## 📈 Future Enhancements

- Multilingual grievance support (Hindi and regional languages)  
- Voice-based complaint submission (speech-to-text)  
- SLA tracking and escalation alerts  
- Analytics dashboard for governance insights  
- Mobile app integration

## 🏆 Hackathon Value Proposition

- Reduces grievance resolution time  
- Improves transparency and accountability  
- Scalable for city, state, and national deployments  
- AI-first approach aligned with Digital India initiatives

## 🙌 Thank You

This project demonstrates how AI can make grievance redressal faster, smarter, and citizen-centric.
