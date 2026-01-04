import streamlit as st
import pandas as pd
from datetime import datetime
import joblib
import os

from utils import (
    get_priority,
    get_department,
    get_sentiment,
    extract_keywords,
    estimate_resolution_time,
    generate_ticket_id,
)
from database import GrievanceDatabase
from report_generator import generate_pdf_report

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Grievance Redressal System",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CSS =================
st.markdown("""
<style>

/* Push app down so header not hidden */
.block-container {
    padding-top: 4.5rem !important;
}

/* Header */
.gov-header {
    width: 100%;
    background: linear-gradient(90deg, #FF6B35, #F7931E);
    color: white;
    text-align: center;
    padding: 22px 10px;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-bottom: 4px solid #138808;
}

/* Tabs full width */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    width: 100%;
}

.stTabs [data-baseweb="tab"] {
    flex-grow: 1;
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    padding: 12px 0;
}

.stTabs [aria-selected="true"] {
    border-bottom: 3px solid #FF6B35 !important;
}

/* Card */
.card {
    background-color: rgba(128,128,128,0.08);
    padding: 2rem;
    border-radius: 12px;
    border-left: 6px solid #FF6B35;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="gov-header">
🇮🇳 Government of India | AI-Powered Grievance Redressal System
</div>
""", unsafe_allow_html=True)
# =====================================================
# HEADER + TOP NAVIGATION
# =====================================================
st.markdown(
    "<div class='gov-header'>🇮🇳 GOVERNMENT OF INDIA | AI-Powered Grievance Redressal System</div>",
    unsafe_allow_html=True
)

st.markdown("<div class='top-nav'>", unsafe_allow_html=True)
page = st.radio(
    "Navigation Menu",
    ["🏠 Submit Complaint", "📊 Dashboard", "🔍 Track Complaint", "⚙️ Admin Panel"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)

# ================= DATABASE & MODEL =================
db = GrievanceDatabase()

@st.cache_resource
def load_model():
    path = "model/classifier.pkl"

    return joblib.load(path) if os.path.exists(path) else None

    if os.path.exists(path):
        return joblib.load(path)
    return None

model = load_model()

def predict_category(text):
    if model:
        try:
            return model.predict([text])[0]
        except:
            return "General"
    return "Administrative"

# ================= TABS =================
tabs = st.tabs([
    "🏠 Submit Complaint",
    "📊 Dashboard",
    "🔍 Track Complaint",
    "⚙️ Admin Panel"
])

# ================= TAB 1 =================
with tabs[0]:
    st.markdown("## Register New Grievance")

    with st.form("grievance_form"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number")

        with col2:
            complaint_text = st.text_area(
                "Complaint Details *",
                height=160,
                placeholder="Describe your grievance clearly..."
            )

        st.markdown("</div>", unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 Submit Official Complaint", use_container_width=True)

    if submit:
        if not name or not email or not complaint_text:
            st.error("Please fill all required fields")
        else:
            category = predict_category(complaint_text)
            priority = get_priority(complaint_text)
            department = get_department(category)
            sentiment = get_sentiment(complaint_text)
            keywords = extract_keywords(complaint_text)
            resolution = estimate_resolution_time(category, priority)
            ticket_id = generate_ticket_id()

            submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            complaint_data = {
                "ticket_id": ticket_id,
                "name": name,
                "email": email,
                "phone": phone or "N/A",
                "complaint_text": complaint_text,
                "category": category,
                "priority": priority,
                "department": department,
                "sentiment_label": sentiment["label"],
                "sentiment_score": sentiment["score"],
                "keywords": ", ".join(keywords),
                "resolution_time": resolution,
                "status": "Pending",
                "submitted_at": submitted_at
            }

            db.add_complaint(complaint_data)

            st.success("✅ Complaint registered successfully")
            st.markdown(f"### 🎫 Ticket ID: `{ticket_id}`")
            st.balloons()

            pdf_path = generate_pdf_report(
                ticket_id,
                {
                    "Name": name,
                    "Email": email,
                    "Phone": phone or "N/A",
                    "Category": category,
                    "Priority": priority,
                    "Department": department,
                    "Sentiment": sentiment["label"],
                    "Keywords": ", ".join(keywords),
                    "Estimated Resolution": resolution,
                    "Status": "Pending",
                    "Submitted At": submitted_at,
                    "Complaint": complaint_text
                }
            )

            with open(pdf_path, "rb") as pdf:
                st.download_button(
                    "📄 Download Complaint PDF",
                    data=pdf,
                    file_name=f"Grievance_{ticket_id}.pdf",
                    mime="application/pdf"
                )

# ================= TAB 2 =================
with tabs[1]:
    data = db.get_all_complaints()
    if data:
        df = pd.DataFrame(data)
        st.bar_chart(df["department"].value_counts())
    else:
        st.info("No complaints yet")

# ================= TAB 3 =================
with tabs[2]:
    ticket = st.text_input("Enter Ticket ID")
    if st.button("Search"):
        res = db.get_complaint_by_ticket(ticket)
        if res:
            st.json(res)
        else:
            st.error("Ticket not found")

# ================= TAB 4 =================
with tabs[3]:
    if "admin" not in st.session_state:
        st.session_state.admin = False

    if not st.session_state.admin:
        pwd = st.text_input("Admin Password", type="password")
        if st.button("Login") and pwd == "admin123":
            st.session_state.admin = True
            st.rerun()
    else:
        st.button("Logout", on_click=lambda: st.session_state.update({"admin": False}))
        st.dataframe(pd.DataFrame(db.get_all_complaints()), use_container_width=True)

# ================= FOOTER =================
st.markdown("<hr><center>🇮🇳 National AI Redressal Framework | 2026</center>", unsafe_allow_html=True)
