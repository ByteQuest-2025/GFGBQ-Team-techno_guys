"""
Quick verification script to check data and installation
"""
import sys

print("=" * 60)
print("🔍 VERIFICATION SCRIPT - Checking Setup")
print("=" * 60)

# Check 1: Data file
print("\n1️⃣ Checking data file...")
try:
    import pandas as pd
    df = pd.read_csv("data/cleaned_data.csv")
    print(f"   ✅ Data loaded successfully!")
    print(f"   ✅ Total rows: {len(df)}")
    print(f"   ✅ Columns: {list(df.columns)}")
    print(f"\n   📊 Category distribution:")
    print(df['category'].value_counts())
except FileNotFoundError:
    print("   ❌ ERROR: data/cleaned_data.csv not found!")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)

# Check 2: Required libraries
print("\n2️⃣ Checking required libraries...")
required = ['pandas', 'sklearn', 'streamlit', 'joblib']
missing = []

for lib in required:
    try:
        if lib == 'sklearn':
            __import__('sklearn')
        else:
            __import__(lib)
        print(f"   ✅ {lib} installed")
    except ImportError:
        print(f"   ❌ {lib} NOT installed")
        missing.append(lib)

if missing:
    print(f"\n⚠️  Missing libraries: {', '.join(missing)}")
    print("   Run: pip install -r requirements.txt")
else:
    print("\n✅ All libraries installed!")

# Check 3: Project structure
print("\n3️⃣ Checking project structure...")
import os

files_to_check = [
    "train_model.py",
    "app.py",
    "utils.py",
    "requirements.txt",
    "README.md"
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} missing")

print("\n" + "=" * 60)
print("📋 SUMMARY")
print("=" * 60)

if not missing and os.path.exists("data/cleaned_data.csv"):
    print("✅ Everything looks good! You're ready to:")
    print("   1. Run: python train_model.py")
    print("   2. Then: streamlit run app.py")
else:
    print("⚠️  Please fix the issues above before proceeding.")

print("=" * 60)
