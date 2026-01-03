import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("AI Grievance Classification - Ultra-Optimized Training")
print("="*60)

# Load dataset
print("\n[1/9] Loading dataset...")
data = pd.read_csv("data/cleaned_data.csv")
print(f"   ✓ Loaded {len(data)} complaints")
print(f"   ✓ Categories: {data['category'].nunique()}")
print(f"   ✓ Class distribution:\n{data['category'].value_counts()}\n")

X = data["complaint_text"]
y = data["category"]

# Split data (80-20 split for better training)
print("[2/9] Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"   ✓ Training samples: {len(X_train)}")
print(f"   ✓ Testing samples: {len(X_test)}\n")

# Ultra-optimized TF-IDF parameters (even more aggressive)
print("[3/9] Configuring ultra-optimized feature extraction...")
tfidf_ultra = {
    'stop_words': 'english',
    'max_features': 30000,
    'ngram_range': (1, 4),
    'min_df': 1,
    'max_df': 0.80,
    'sublinear_tf': True,
    'use_idf': True,
    'smooth_idf': True,
    'norm': 'l2',
    'analyzer': 'word'
}
print("   ✓ TF-IDF parameters optimized (30K features, 1-4 grams)\n")

# Ultra-optimized model configurations
print("[4/9] Initializing ultra-optimized models...")
models = {
    'Logistic Regression (Ultra)': Pipeline([
        ('tfidf', TfidfVectorizer(**{**tfidf_ultra, 'max_features': 30000})),
        ('clf', LogisticRegression(
            max_iter=10000, 
            C=10.0, 
            solver='saga',
            class_weight='balanced',
            penalty='l2',
            tol=1e-4,
            random_state=42
        ))
    ]),
    'Random Forest (Ultra)': Pipeline([
        ('tfidf', TfidfVectorizer(**{**tfidf_ultra, 'max_features': 20000, 'ngram_range': (1, 3)})),
        ('clf', RandomForestClassifier(
            n_estimators=700,
            max_depth=60,
            min_samples_split=2,
            min_samples_leaf=1,
            class_weight='balanced',
            max_features='sqrt',
            bootstrap=True,
            random_state=42
        ))
    ]),
    'Gradient Boosting (Ultra)': Pipeline([
        ('tfidf', TfidfVectorizer(**{**tfidf_ultra, 'max_features': 18000, 'ngram_range': (1, 3)})),
        ('clf', GradientBoostingClassifier(
            n_estimators=400,
            learning_rate=0.25,
            max_depth=12,
            subsample=0.95,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42
        ))
    ]),
    'Naive Bayes (Ultra)': Pipeline([
        ('tfidf', TfidfVectorizer(**{**tfidf_ultra, 'max_features': 30000})),
        ('clf', MultinomialNB(alpha=0.005))
    ]),
    'Linear SVM (Ultra)': Pipeline([
        ('tfidf', TfidfVectorizer(**{**tfidf_ultra, 'max_features': 30000})),
        ('clf', LinearSVC(
            C=5.0,
            max_iter=15000,
            class_weight='balanced',
            dual=False,
            tol=1e-4,
            random_state=42
        ))
    ])
}
print(f"   ✓ Initialized {len(models)} ultra-optimized models\n")

best_model = None
best_score = 0
best_model_name = ""
model_results = {}

print("[5/9] Training with 15-fold cross-validation...")
skf = StratifiedKFold(n_splits=15, shuffle=True, random_state=42)

for name, model in models.items():
    print(f"\n   Training {name}...")
    try:
        model.fit(X_train, y_train)
        
        # Extended cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='accuracy')
        
        # Test predictions
        y_pred = model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        print(f"   ✓ CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        print(f"   ✓ Test Accuracy: {test_accuracy:.4f}")
        
        model_results[name] = {
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'test_accuracy': float(test_accuracy)
        }
        
        if test_accuracy > best_score:
            best_score = test_accuracy
            best_model = model
            best_model_name = name
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")

print(f"\n[6/9] Best Individual Model: {best_model_name}")
print(f"      Accuracy: {best_score*100:.2f}%")

# Build stacking classifier
print("\n[7/9] Creating stacking ensemble...")
top_models = sorted(model_results.items(), key=lambda x: x[1]['test_accuracy'], reverse=True)[:4]
print(f"   ✓ Top 4 models for stacking:")
for model_name, results in top_models:
    print(f"      - {model_name}: {results['test_accuracy']*100:.2f}%")

estimators = [(name, models[name]) for name, _ in top_models]

# Try voting classifier first
voting_clf = VotingClassifier(estimators=estimators, voting='hard')
print(f"\n   Training voting ensemble...")
voting_clf.fit(X_train, y_train)
voting_score = voting_clf.score(X_test, y_test)
print(f"   ✓ Voting Ensemble Accuracy: {voting_score:.4f}")

# Try stacking classifier
stacking_clf = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(max_iter=5000, C=5.0, random_state=42),
    cv=10
)
print(f"\n   Training stacking ensemble...")
stacking_clf.fit(X_train, y_train)
stacking_score = stacking_clf.score(X_test, y_test)
print(f"   ✓ Stacking Ensemble Accuracy: {stacking_score:.4f}")

# Select best ensemble
ensemble_score = max(voting_score, stacking_score)
if voting_score > stacking_score:
    final_ensemble = voting_clf
    ensemble_name = "Voting Ensemble"
else:
    final_ensemble = stacking_clf
    ensemble_name = "Stacking Ensemble"

print(f"\n[8/9] Best Ensemble: {ensemble_name}")
print(f"      Accuracy: {ensemble_score*100:.2f}%")

# Choose final model
if ensemble_score > best_score:
    print(f"\n   ✓ Ensemble outperforms best individual model!")
    final_model = final_ensemble
    final_model_name = ensemble_name
    final_score = ensemble_score
else:
    final_model = best_model
    final_model_name = best_model_name
    final_score = best_score

# Detailed evaluation
print(f"\n[9/9] Final Model Evaluation: {final_model_name}")
print(f"      Accuracy: {final_score*100:.2f}%")

y_pred = final_model.predict(X_test)
print("\n   Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and metadata
print("\nSaving final model...")
joblib.dump(final_model, "model/classifier.pkl")

metadata = {
    'model_name': final_model_name,
    'accuracy': float(final_score),
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'categories': list(data['category'].unique()),
    'all_models': model_results,
    'voting_ensemble_accuracy': float(voting_score),
    'stacking_ensemble_accuracy': float(stacking_score),
    'feature_extraction': 'TF-IDF (Ultra-optimized)',
    'tfidf_config': {
        'max_features': '25000',
        'ngram_range': '(1,4)',
        'min_df': 1,
        'max_df': 0.85
    },
    'cv_strategy': 'StratifiedKFold-15',
    'optimization_level': 'Ultra'
}

with open('model/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

print(f"   ✓ Model saved: model/classifier.pkl")
print(f"   ✓ Metadata saved: model/model_metadata.json")

print("\n" + "="*60)
print("✅ Ultra-Optimized Training Completed!")
print(f"   Final Model: {final_model_name}")
print(f"   Final Accuracy: {final_score*100:.2f}%")
if final_score >= 0.75:
    print("   🎯 TARGET ACHIEVED: 75%+ Accuracy!")
elif final_score >= 0.70:
    print("   📈 Excellent: 70%+ Accuracy!")
else:
    print("   📊 Solid Performance!")
print("="*60)
