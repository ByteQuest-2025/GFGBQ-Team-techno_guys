import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Load dataset
data = pd.read_csv("data/cleaned_data.csv")

X = data["complaint_text"]
y = data["category"]

# Create ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train model
model.fit(X, y)

# Save model
joblib.dump(model, "model/classifier.pkl")

print("Model trained and saved successfully!")
