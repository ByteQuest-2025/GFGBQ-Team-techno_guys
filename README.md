# GFGBQ — Team techno_guys

Repository for Team techno_guys — Vibe Coding Hackathon

## 📌 Problem Statement

**PS-12: AI for Grievance Redressal in Public Governance**

Government bodies receive thousands of citizen grievances daily related to infrastructure, sanitation, healthcare, public safety, utilities, and administrative delays. These grievances are often unstructured (free text, mixed languages) and manually processed, which slows resolution. The lack of intelligent prioritization and routing causes delayed resolution of critical issues, citizen dissatisfaction, and reduced transparency.

There is a need for an AI-powered system that can automatically analyze, classify, prioritize, and route grievances to enable faster, fairer, and more accountable governance.

## 🚀 Project Name

**SmartGov AI — Intelligent Grievance Redressal System**

## 👥 Team

**Team techno_guys**

## 🌐 Deployed Link (optional)

`https://your-deployed-link.com`

## 🎥 2-Minute Demonstration Video (optional)

`https://your-demo-video-link.com`  
(YouTube unlisted / Google Drive)

## 📊 Presentation (optional)

`https://your-ppt-link.com`  
(Google Slides / Drive)
 ok

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

- Backend: Streamlit (Python)  
- AI / ML: Python, scikit-learn, TF-IDF Vectorizer, Logistic Regression  
- Dataset: Structured grievance dataset (CSV)
- Libraries: pandas, joblib, NLTK

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/ByteQuest-2025/GFGBQ-Team-techno_guys
cd GFGBQ-Team-techno_guys
```

### 2. Create and activate a virtual environment (recommended)

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (cmd.exe):**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the setup

Run the verification script to check if everything is set up correctly:

```bash
python verify_setup.py
```

This will check:
- Data file availability (`data/cleaned_data.csv`)
- Required libraries installation
- Project structure

### 5. Prepare your data

Place your grievance dataset in the `data/` folder as `cleaned_data.csv`. The CSV should have at least these columns:
- `complaint_text`: The grievance text
- `category`: The category label (e.g., Sanitation, Healthcare, Infrastructure, etc.)

Refer to [DATA_PREPARATION_GUIDE.md](DATA_PREPARATION_GUIDE.md) for detailed data preparation instructions.

### 6. Train the model

```bash
python train_model.py
```

This will:
- Load the data from `data/cleaned_data.csv`
- Train a Logistic Regression model with TF-IDF features
- Save the trained model to `model/classifier.pkl`

### 7. Run the Streamlit application

```bash
streamlit run app.py
```

The application will run at: <http://localhost:8501>

## ▶️ Usage

1. Open your browser and navigate to <http://localhost:8501>
2. Enter a grievance in the text area (e.g., "Garbage not collected for 7 days")
3. Click the "Analyze Complaint" button
4. The AI system will:
   - Classify the grievance into a category (Sanitation, Healthcare, Infrastructure, etc.)
   - Determine the priority level (Critical or Normal) based on keywords
   - Assign it to the relevant department

## 🧠 How It Work

The system uses a machine learning pipeline with:
- **TF-IDF Vectorizer**: Converts text complaints into numerical features
- **Logistic Regression**: Classifies complaints into categories
- Trained on labeled grievance data

### Priority Detection (`utils.py`)

Keywords are analyzed to determine urgency:
- **Critical**: Contains words like "accident", "emergency", "hospital", "fire", "danger", "life", "death"
- **Normal**: All other complaints

### Department Routing (`utils.py`)

Each category is mapped to the appropriate department:
- Sanitation → Municipal Sanitation Department
- Utilities → Electricity / Water Department
- Healthcare → Health Department
- Public Safety → Police Department
- Infrastructure → Public Works Department
- Administration → District Administration

## � Project Structure

```
grievance_ai_project/
├── app.py                      # Streamlit web application
├── train_model.py              # Model training script
├── utils.py                    # Helper functions (priority & department mapping)
├── verify_setup.py             # Setup verification script
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── DATA_PREPARATION_GUIDE.md   # Data preparation instructions
├── data/
│   ├── cleaned_data.csv        # Training dataset
│   └── sample_cleaned_data.csv # Sample data (if available)
└── model/
    └── classifier.pkl          # Trained model (generated after training)
```

## 📸 Screenshots

- Grievance Submission Interface  
- AI Classification & Priority Output  
- Department Assignment

(Add screenshots as needed)

## 📈 Future Enhancements

- Enhanced ML models (Random Forest, Gradient Boosting, or Deep Learning)
- Multilingual grievance support (Hindi and regional languages)  
- Voice-based complaint submission (speech-to-text)  
- Real-time dashboard for monitoring grievances
- SLA tracking and escalation alerts  
- Analytics dashboard for governance insights  
- Mobile app integration
- Integration with government grievance portals

## 🏆 Hackathon Value Proposition

- Reduces grievance resolution time  
- Improves transparency and accountability  
- Scalable for city, state, and national deployments  
- AI-first approach aligned with Digital India initiatives

## 🙌 Thank You

This project demonstrates how AI can make grievance redressal faster, smarter, and citizen-centric.