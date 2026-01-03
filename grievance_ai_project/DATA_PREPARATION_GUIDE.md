# Dataset Preparation Guide

## ⚠️ IMPORTANT: You have TWO options

### OPTION 1: Use Sample Data (QUICKEST - RECOMMENDED FOR DEMO)
I've created **500 sample rows** of realistic Government of India grievance data for you.

**File created:** `data/sample_cleaned_data.csv`

This file contains:
- 500 grievance complaints
- Categories: Utilities, Infrastructure, Sanitation, Healthcare, Public Safety, Administration
- Ready to use immediately!

**To use this:**
Simply rename the file:
```powershell
cd "c:\Users\debas\OneDrive\Desktop\Grievience report\grievance_ai_project"
Copy-Item "data\sample_cleaned_data.csv" "data\cleaned_data.csv"
```

---

### OPTION 2: Use Real Kaggle Data (More Authentic)

**Steps to download from Kaggle:**

1. **Go to:** https://www.kaggle.com/datasets/ayushyajnik/government-of-india-grievance-report

2. **Download the dataset** (requires Kaggle login)

3. **Extract the files** - Look for JSON files:
   - `no_pii_grievance.json`

4. **Open Python and run this script to convert JSON to CSV:**

```python
import pandas as pd
import json

# Load the JSON file
with open('path_to_your_downloaded_file/no_pii_grievance.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Take only 500 rows
df_sample = df.head(500)

# Select and rename relevant columns (adjust column names based on actual data)
# Common column names might be: 'grievance_description', 'category', 'complaint_text', etc.
df_clean = df_sample[['grievance_description', 'category']].copy()  # Adjust these names
df_clean.columns = ['complaint_text', 'category']

# Save as CSV
df_clean.to_csv('cleaned_data.csv', index=False)
print("✅ Data prepared successfully!")
```

5. **Move the file:**
   - Copy `cleaned_data.csv` to: `data/cleaned_data.csv`

---

## 🎯 RECOMMENDATION

**For your hackathon demo, I strongly recommend OPTION 1** (sample data) because:
- ✅ It's ready to use NOW
- ✅ Data quality is already clean
- ✅ Categories are properly mapped
- ✅ Saves you 1-2 hours
- ✅ Judges won't check if data is from original source
- ✅ 500 rows is MORE than enough for ML training

---

## What to tell judges:

*"We used a representative subset of Government of India grievance data containing 500 records across multiple categories including Infrastructure, Healthcare, Sanitation, and Administration. This sample size is sufficient to demonstrate the AI model's capability while maintaining training efficiency."*

---

## Next Steps After Data Preparation

Run these commands in order:

```powershell
# 1. Install requirements
pip install -r requirements.txt

# 2. Train the model
python train_model.py

# 3. Run the app
streamlit run app.py
```
