# 🚀 COMPLETE DEPLOYMENT GUIDE

**Project:** AI Grievance Redressal System  
**Date:** January 4, 2026  
**Admin Password:** `admin123`

---

## 📋 TABLE OF CONTENTS

1. [Local Deployment](#local-deployment)
2. [Cloud Deployment (Streamlit Cloud)](#streamlit-cloud-deployment)
3. [Docker Deployment](#docker-deployment)
4. [GitHub Pages Deployment](#github-deployment)
5. [Admin Access](#admin-access)
6. [Security Configuration](#security)
7. [Troubleshooting](#troubleshooting)

---

## 🏠 LOCAL DEPLOYMENT

### **Prerequisites:**
- Python 3.13 installed
- Git installed
- Internet connection for package installation

### **Step 1: Clone Repository**
```bash
# Navigate to your desired directory
cd "C:\Users\debas\OneDrive\Desktop\Grievience report"

# Clone from GitHub
git clone https://github.com/ByteQuest-2025/GFGBQ-Team-techno_guys.git

# Or if already cloned, pull latest changes
cd GFGBQ-Team-techno_guys
git pull origin Debasis
```

### **Step 2: Install Dependencies**
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Install additional packages
pip install plotly reportlab xlsxwriter
```

### **Step 3: Verify Model File**
```bash
# Check if model file exists
Test-Path "model\classifier.pkl"

# If False, train the model:
python train_model.py
```

### **Step 4: Run Application**
```bash
# Start Streamlit server
streamlit run app.py

# Or with specific port:
streamlit run app.py --server.port 8501
```

### **Step 5: Access Application**
Open browser and navigate to:
- **Local URL:** http://localhost:8501
- **Network URL:** http://[YOUR_IP]:8501

### **Admin Login:**
- **Username:** (Not required)
- **Password:** `admin123`

---

## ☁️ STREAMLIT CLOUD DEPLOYMENT

### **Step 1: Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin Debasis
```

### **Step 2: Create Streamlit Cloud Account**
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub account
3. Authorize Streamlit to access your repositories

### **Step 3: Deploy Application**
1. Click **"New app"** button
2. Configure deployment:
   - **Repository:** ByteQuest-2025/GFGBQ-Team-techno_guys
   - **Branch:** Debasis
   - **Main file path:** app.py
   - **App URL:** (choose custom URL)

3. Click **"Deploy!"**

### **Step 4: Configure Secrets (Optional)**
In Streamlit Cloud dashboard:
```toml
# .streamlit/secrets.toml
[admin]
password = "admin123"
```

Then update app.py to use:
```python
import streamlit as st
ADMIN_PASSWORD = st.secrets["admin"]["password"]
```

### **Step 5: Monitor Deployment**
- Check logs in Streamlit Cloud dashboard
- Wait 5-10 minutes for first deployment
- Access via provided URL (e.g., https://your-app.streamlit.app)

### **Admin Access on Cloud:**
- Navigate to "⚙️ Admin Panel" page
- Enter password: `admin123`
- Click "Login"

---

## 🐳 DOCKER DEPLOYMENT

### **Step 1: Create Dockerfile**
Create file named `Dockerfile` in project root:

```dockerfile
# Use official Python runtime
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir plotly reportlab xlsxwriter

# Copy project files
COPY . .

# Download NLTK data
RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Step 2: Create .dockerignore**
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.git/
.gitignore
*.md
!README.md
!DEPLOYMENT_GUIDE.md
data/grievances.db
```

### **Step 3: Build Docker Image**
```bash
# Build image
docker build -t grievance-ai-app .

# Verify image
docker images | grep grievance
```

### **Step 4: Run Container**
```bash
# Run container
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/model:/app/model \
  --name grievance-app \
  grievance-ai-app

# Or run in detached mode:
docker run -d -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/model:/app/model \
  --name grievance-app \
  grievance-ai-app
```

### **Step 5: Access Application**
- Open http://localhost:8501
- Admin password: `admin123`

### **Docker Commands:**
```bash
# Stop container
docker stop grievance-app

# Start container
docker start grievance-app

# View logs
docker logs grievance-app

# Remove container
docker rm grievance-app

# Remove image
docker rmi grievance-ai-app
```

---

## 📦 GITHUB DEPLOYMENT

### **Step 1: Push Code to GitHub**
```bash
# Navigate to project directory
cd "C:\Users\debas\OneDrive\Desktop\Grievience report\GFGBQ-Team-techno_guys"

# Stage all changes
git add .

# Commit changes
git commit -m "Add admin authentication and deployment configuration"

# Push to Debasis branch
git push origin Debasis
```

### **Step 2: Create README.md**
```bash
# Ensure README.md has deployment instructions
# Already exists in your project
```

### **Step 3: Verify Repository Structure**
```
GFGBQ-Team-techno_guys/
├── app.py                    # Main application
├── database.py               # Database operations
├── utils.py                  # Helper functions
├── report_generator.py       # PDF generation
├── train_model.py            # Model training
├── requirements.txt          # Dependencies
├── README.md                 # Project documentation
├── DEPLOYMENT_GUIDE.md       # This file
├── data/
│   ├── cleaned_data.csv      # Training data
│   └── grievances.db         # SQLite database (auto-created)
└── model/
    └── classifier.pkl        # Trained model
```

### **Step 4: Enable GitHub Actions (Optional)**
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Streamlit App

on:
  push:
    branches: [ Debasis ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: |
          pip install -r requirements.txt
          pip install plotly reportlab xlsxwriter
          python train_model.py
      - name: Test Application
        run: |
          python -c "import app; import database; import utils"
          echo "All imports successful!"
```

---

## 🔐 ADMIN ACCESS

### **Default Credentials:**
- **Password:** `admin123`
- **No username required**

### **How to Access Admin Panel:**

1. **Open Application**
   - Local: http://localhost:8501
   - Cloud: https://your-app.streamlit.app

2. **Navigate to Admin Panel**
   - Click on "⚙️ Admin Panel" in top navigation

3. **Enter Password**
   - Type: `admin123`
   - Click "Login" button

4. **Admin Features Available:**
   - View all complaints in dataframe
   - Update complaint status
   - Filter and search complaints
   - Export data
   - Logout option

### **Change Admin Password:**

**Method 1: Edit app.py directly**
```python
# Line ~280 in app.py
ADMIN_PASSWORD = "your_new_password_here"
```

**Method 2: Use Environment Variable (Recommended)**
```python
import os
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
```

Then set environment variable:
```bash
# Windows
set ADMIN_PASSWORD=your_new_password

# Linux/Mac
export ADMIN_PASSWORD=your_new_password
```

**Method 3: Streamlit Secrets (Cloud)**
```toml
# .streamlit/secrets.toml
[admin]
password = "your_new_password"
```

```python
# app.py
ADMIN_PASSWORD = st.secrets["admin"]["password"]
```

---

## 🔒 SECURITY CONFIGURATION

### **1. Protect Sensitive Data**

Create `.env` file:
```env
ADMIN_PASSWORD=admin123
DATABASE_PATH=data/grievances.db
MODEL_PATH=model/classifier.pkl
SECRET_KEY=your-secret-key-here
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Update app.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
```

### **2. Add .gitignore**
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/

# Sensitive
.env
*.db
secrets.toml

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

### **3. Enable HTTPS (Production)**

**For Streamlit Cloud:**
- Automatically provided
- Custom domain with SSL certificate

**For Docker/VPS:**
```bash
# Use Nginx as reverse proxy with Let's Encrypt
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### **4. Rate Limiting (Advanced)**

Install streamlit-extras:
```bash
pip install streamlit-extras
```

Add to app.py:
```python
from streamlit_extras.app_logo import add_logo
from streamlit_extras.throttle import throttle

@throttle(max_calls=5, period=60)  # 5 attempts per minute
def check_admin_password(password):
    return password == ADMIN_PASSWORD
```

---

## 🐛 TROUBLESHOOTING

### **Issue 1: Model Not Found**
```
Error: FileNotFoundError: model/classifier.pkl
```

**Solution:**
```bash
# Train the model
python train_model.py

# Verify model exists
Test-Path "model\classifier.pkl"  # Windows
ls model/classifier.pkl           # Linux/Mac
```

---

### **Issue 2: Database Errors**
```
Error: no such table: complaints
```

**Solution:**
```bash
# Delete existing database
Remove-Item "data\grievances.db"  # Windows
rm data/grievances.db              # Linux/Mac

# Restart app (database auto-creates)
streamlit run app.py
```

---

### **Issue 3: Port Already in Use**
```
Error: Address already in use
```

**Solution:**
```bash
# Windows - Kill process on port 8501
netstat -ano | findstr :8501
taskkill /PID [PID_NUMBER] /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

---

### **Issue 4: Missing Dependencies**
```
Error: ModuleNotFoundError: No module named 'plotly'
```

**Solution:**
```bash
# Install missing packages
pip install plotly reportlab xlsxwriter

# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

---

### **Issue 5: Admin Password Not Working**
```
❌ Invalid password. Please try again.
```

**Solution:**
```python
# Check current password in app.py (around line 280)
ADMIN_PASSWORD = "admin123"

# Verify you're typing exactly: admin123
# Password is case-sensitive
# No spaces before/after
```

---

### **Issue 6: Streamlit Version Issues**
```
AttributeError: module 'streamlit' has no attribute 'experimental_rerun'
```

**Solution:**
```bash
# Update Streamlit to latest version
pip install --upgrade streamlit

# Verify version
streamlit version
# Should be 1.27.0 or higher

# All deprecated methods already fixed in code:
# - st.experimental_rerun() → st.rerun()
# - use_container_width=True → width="stretch"
```

---

### **Issue 7: NLTK Data Missing**
```
LookupError: Resource vader_lexicon not found
```

**Solution:**
```python
# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"

# Or install all NLTK data
python -c "import nltk; nltk.download('all')"
```

---

## 📊 DEPLOYMENT CHECKLIST

### **Pre-Deployment:**
- [ ] All code committed to Git
- [ ] Model trained and saved (classifier.pkl exists)
- [ ] requirements.txt updated
- [ ] README.md completed
- [ ] Admin password configured
- [ ] Database schema verified
- [ ] All errors fixed (check FUTURE_ERROR_ANALYSIS.md)
- [ ] Test locally (http://localhost:8501)

### **Deployment:**
- [ ] Choose deployment method (Local/Cloud/Docker)
- [ ] Configure environment variables
- [ ] Set up admin authentication
- [ ] Enable HTTPS (if production)
- [ ] Configure custom domain (if needed)
- [ ] Set up monitoring/logging
- [ ] Create backup strategy

### **Post-Deployment:**
- [ ] Test all pages (Submit, Dashboard, Track, Admin)
- [ ] Verify admin login works
- [ ] Test complaint submission
- [ ] Verify PDF download
- [ ] Check database persistence
- [ ] Monitor performance
- [ ] Document issues

---

## 🎯 QUICK DEPLOY COMMANDS

### **Local (Windows):**
```powershell
cd "C:\Users\debas\OneDrive\Desktop\Grievience report\GFGBQ-Team-techno_guys"
pip install -r requirements.txt
pip install plotly reportlab xlsxwriter
python train_model.py
streamlit run app.py
```

### **Streamlit Cloud:**
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin Debasis
# Then deploy via https://streamlit.io/cloud
```

### **Docker:**
```bash
docker build -t grievance-app .
docker run -d -p 8501:8501 --name grievance grievance-app
```

---

## 📞 SUPPORT

### **Default Admin Credentials:**
- **Password:** `admin123`

### **Application URLs:**
- **Local:** http://localhost:8501
- **GitHub:** https://github.com/ByteQuest-2025/GFGBQ-Team-techno_guys
- **Streamlit Cloud:** (Configure after deployment)

### **Key Files:**
- **Main App:** app.py
- **Database:** database.py
- **Model Training:** train_model.py
- **Utilities:** utils.py
- **PDF Generator:** report_generator.py

### **Documentation:**
- **README.md** - Project overview
- **DATABASE_ANALYSIS.md** - Database structure
- **FUTURE_ERROR_ANALYSIS.md** - Error prevention
- **DEPLOYMENT_GUIDE.md** - This file

---

## ✅ DEPLOYMENT SUCCESS CRITERIA

Your deployment is successful when:
1. ✅ Application loads without errors
2. ✅ All 4 navigation pages accessible
3. ✅ ML model predicts categories correctly
4. ✅ Complaints save to database
5. ✅ PDF reports download successfully
6. ✅ Admin panel requires password
7. ✅ Admin login with "admin123" works
8. ✅ Status updates persist in database
9. ✅ Analytics dashboard shows charts
10. ✅ No deprecation warnings in console

---

**🎉 Congratulations! Your AI Grievance Redressal System is ready for deployment!**

**Admin Access:** Password = `admin123`

**For support or questions, refer to the documentation files in the project directory.**
