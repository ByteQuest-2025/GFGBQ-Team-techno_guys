import re
from datetime import datetime
import nltk
from collections import Counter

# Download required NLTK data (run once)
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    SENTIMENT_AVAILABLE = True
except:
    SENTIMENT_AVAILABLE = False


def get_priority(text):
    """Determine complaint priority based on keywords and urgency."""
    text = text.lower()
    
    # Critical keywords (life-threatening, immediate danger)
    critical_keywords = [
        "emergency", "urgent", "critical", "danger", "life", "death",
        "fire", "accident", "collapse", "explosion", "injury", "bleeding",
        "attack", "threat", "severe", "crisis"
    ]
    
    # High priority keywords
    high_keywords = [
        "hospital", "broken", "damaged", "leak", "flooding",
        "contaminated", "unsafe", "risk", "hazard", "exposed"
    ]
    
    # Medium priority keywords
    medium_keywords = [
        "problem", "issue", "concern", "need", "require",
        "poor", "inadequate", "insufficient", "delayed"
    ]
    
    # Check for critical
    for word in critical_keywords:
        if word in text:
            return "Critical"
    
    # Check for high
    high_count = sum(1 for word in high_keywords if word in text)
    if high_count >= 2:
        return "High"
    
    # Check for medium
    medium_count = sum(1 for word in medium_keywords if word in text)
    if medium_count >= 2:
        return "Medium"
    
    return "Low"


def get_department(category):
    """Map category to responsible department."""
    mapping = {
        "Sanitation": "Municipal Sanitation Department",
        "Utilities": "Electricity & Water Department",
        "Healthcare": "Health & Medical Services",
        "Public Safety": "Police & Security Department",
        "Infrastructure": "Public Works Department",
        "Administration": "District Administration Office"
    }
    return mapping.get(category, "General Administration")


def get_sentiment(text):
    """Analyze sentiment of the complaint."""
    if not SENTIMENT_AVAILABLE:
        return {"label": "Neutral", "score": 0.0}
    
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    
    return {
        "label": label,
        "score": round(compound, 3),
        "positive": round(scores['pos'], 3),
        "negative": round(scores['neg'], 3),
        "neutral": round(scores['neu'], 3)
    }


def extract_keywords(text, top_n=5):
    """Extract important keywords from complaint."""
    # Remove common words
    stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 
                  'in', 'with', 'to', 'for', 'of', 'as', 'by', 'this', 'that',
                  'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do',
                  'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might'}
    
    # Tokenize and clean
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    filtered_words = [w for w in words if w not in stop_words]
    
    # Count frequency
    word_freq = Counter(filtered_words)
    return [word for word, _ in word_freq.most_common(top_n)]


def estimate_resolution_time(category, priority):
    """Estimate resolution time based on category and priority."""
    # Base resolution times (in hours)
    base_times = {
        "Sanitation": 24,
        "Utilities": 48,
        "Healthcare": 12,
        "Public Safety": 6,
        "Infrastructure": 72,
        "Administration": 96
    }
    
    # Priority multipliers
    priority_multipliers = {
        "Critical": 0.25,
        "High": 0.5,
        "Medium": 1.0,
        "Low": 1.5
    }
    
    base = base_times.get(category, 48)
    multiplier = priority_multipliers.get(priority, 1.0)
    hours = int(base * multiplier)
    
    if hours < 24:
        return f"{hours} hours"
    else:
        days = hours // 24
        return f"{days} days"


def generate_ticket_id():
    """Generate unique ticket ID."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    import random
    random_suffix = random.randint(1000, 9999)
    return f"GRV-{timestamp}-{random_suffix}"


def get_contact_info(department):
    """Get contact information for department."""
    contacts = {
        "Municipal Sanitation Department": {
            "phone": "+91-1234-567890",
            "email": "sanitation@municipality.gov.in",
            "office_hours": "9:00 AM - 6:00 PM"
        },
        "Electricity & Water Department": {
            "phone": "+91-1234-567891",
            "email": "utilities@municipality.gov.in",
            "office_hours": "24/7 Emergency Hotline"
        },
        "Health & Medical Services": {
            "phone": "+91-1234-567892",
            "email": "health@municipality.gov.in",
            "office_hours": "24/7 Emergency Services"
        },
        "Police & Security Department": {
            "phone": "100 (Emergency)",
            "email": "security@police.gov.in",
            "office_hours": "24/7 Emergency Hotline"
        },
        "Public Works Department": {
            "phone": "+91-1234-567893",
            "email": "pwd@municipality.gov.in",
            "office_hours": "9:00 AM - 6:00 PM"
        },
        "District Administration Office": {
            "phone": "+91-1234-567894",
            "email": "admin@district.gov.in",
            "office_hours": "9:00 AM - 5:00 PM"
        }
    }
    return contacts.get(department, {
        "phone": "+91-1234-567800",
        "email": "grievance@municipality.gov.in",
        "office_hours": "9:00 AM - 5:00 PM"
    })
