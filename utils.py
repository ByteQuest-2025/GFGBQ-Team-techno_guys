def get_priority(text):
    text = text.lower()

    critical_keywords = [
        "accident", "emergency", "hospital",
        "fire", "danger", "life", "death"
    ]

    for word in critical_keywords:
        if word in text:
            return "Critical"

    return "Normal"


def get_department(category):
    mapping = {
        "Sanitation": "Municipal Sanitation Department",
        "Utilities": "Electricity / Water Department",
        "Healthcare": "Health Department",
        "Public Safety": "Police Department",
        "Infrastructure": "Public Works Department",
        "Administration": "District Administration"
    }

    return mapping.get(category, "General Administration")
