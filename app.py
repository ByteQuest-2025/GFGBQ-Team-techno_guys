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

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Grievance Redressal System",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# GOVERNMENT PORTAL CSS
# =====================================================
st.markdown("""
<style>

/* Background & Font */
.stApp {
    background-color: #F5F7FA;
    font-family: 'Segoe UI', sans-serif;
}

/* Hide sidebar completely */
[data-testid="stSidebar"] {
    display: none;
}

/* Government Header */
.gov-header {
    background: linear-gradient(90deg, #FF6B35, #F7931E);
    color: white;
    padding: 14px;
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin: -70px -70px 0 -70px;
}

/* Top Navigation Bar */
.top-nav {
    background: white;
    border-bottom: 3px solid #FF6B35;
    margin: 0 -70px 25px -70px;
}

.top-nav [role="radiogroup"] {
    display: flex;
    justify-content: center;
}

.top-nav label {
    padding: 16px 36px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #2C3E50 !important;
    border-right: 1px solid #E0E0E0 !important;
}

.top-nav label[data-selected="true"] {
    background-color: #FF6B35 !important;
    color: white !important;
}

/* Cards */
.card {
    background: white;
    border-radius: 10px;
    padding: 24px;
    border-left: 5px solid #FF6B35;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Headings */
h1 { font-size: 32px; color: #2C3E50; }
h2 { font-size: 24px; color: #FF6B35; }
h3 { font-size: 18px; color: #2C3E50; }

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #FF6B35, #F7931E);
    color: white;
    font-size: 15px;
    font-weight: 600;
    border-radius: 6px;
    padding: 10px 30px;
    border: none;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 26px;
    font-weight: 700;
    color: #FF6B35;
}

</style>
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

# =====================================================
# DATABASE & MODEL
# =====================================================
db = GrievanceDatabase()

@st.cache_resource
def load_model():
    path = "model/classifier.pkl"
    if os.path.exists(path):
        return joblib.load(path)
    return None

model = load_model()

def predict_category(text):
    if model:
        return model.predict([text])[0]
    return "Administrative"

# =====================================================
# 🏠 SUBMIT COMPLAINT
# =====================================================
if page == "🏠 Submit Complaint":

    st.markdown("# Submit Your Grievance")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone (Optional)")

    with col2:
        complaint_text = st.text_area("Describe your complaint", height=180)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Submit Complaint"):
        if not name or not email or not complaint_text:
            st.warning("Please fill all required fields")
        else:
            with st.spinner("Processing with AI..."):
                category = predict_category(complaint_text)
                priority = get_priority(complaint_text)
                department = get_department(category)
                sentiment = get_sentiment(complaint_text)
                keywords = extract_keywords(complaint_text)
                resolution_time = estimate_resolution_time(category, priority)
                ticket_id = generate_ticket_id()

                data = {
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
                    "resolution_time": resolution_time,
                    "status": "Pending",
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                db.add_complaint(data)

            st.success("Complaint submitted successfully")
            st.balloons()

            col1, col2, col3 = st.columns(3)
            col1.metric("Ticket ID", ticket_id)
            col2.metric("Priority", priority)
            col3.metric("Department", department)

            pdf = generate_pdf_report(data, ticket_id)
            st.download_button(
                "Download PDF Report",
                pdf,
                file_name=f"{ticket_id}.pdf",
                mime="application/pdf"
            )

# =====================================================
# 📊 DASHBOARD
# =====================================================
elif page == "📊 Dashboard":

    st.markdown("# Analytics Dashboard")

    complaints = db.get_all_complaints()
    if not complaints:
        st.info("No complaints yet")
    else:
        df = pd.DataFrame(complaints)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Complaints", len(df))
        col2.metric("Pending", (df["status"] == "Pending").sum())
        col3.metric("Resolved", (df["status"] == "Resolved").sum())

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Complaints by Category")
        st.bar_chart(df["category"].value_counts())
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Priority Distribution")
        st.bar_chart(df["priority"].value_counts())
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# 🔍 TRACK COMPLAINT
# =====================================================
elif page == "🔍 Track Complaint":

    st.markdown("# Track Your Complaint")

    ticket = st.text_input("Enter Ticket ID")

    if st.button("Track Complaint"):
        result = db.get_complaint_by_ticket(ticket)
        if not result:
            st.error("Ticket ID not found")
        else:
            # result is already a dictionary, no need for [0]
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write(f"**Name:** {result['name']}")
            st.write(f"**Status:** {result['status']}")
            st.write(f"**Priority:** {result['priority']}")
            st.write(f"**Department:** {result['department']}")
            st.info(result["complaint_text"])
            st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ⚙️ ADMIN PANEL (PASSWORD PROTECTED)
# =====================================================
elif page == "⚙️ Admin Panel":

    st.markdown("# 🔐 Admin Control Panel")
    
    # Initialize session state for authentication
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    # Admin password (in production, use environment variable)
    ADMIN_PASSWORD = "admin123"
    
    # Authentication check
    if not st.session_state.admin_authenticated:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🔒 Authentication Required")
        st.info("Please enter the admin password to access the control panel")
        
        password = st.text_input("Enter Admin Password", type="password", key="admin_password")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Login", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password. Please try again.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Default Admin Credentials:**")
        st.code("Password: admin123", language="text")
        
    else:
        # Admin is authenticated - show panel
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🚪 Logout"):
                st.session_state.admin_authenticated = False
                st.rerun()
        
        complaints = db.get_all_complaints()
        if not complaints:
            st.info("No complaints available")
        else:
            df = pd.DataFrame(complaints)
            st.dataframe(df, width="stretch")

            st.markdown("## Update Complaint Status")
            ticket = st.text_input("Ticket ID")
            new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])

            if st.button("Update Status"):
                if db.update_complaint_status(ticket, new_status):
                    st.success("Status updated successfully")
                    st.rerun()
                else:
                    st.error("Invalid Ticket ID")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(
    "<center>🇮🇳 AI-Powered Grievance Redressal System | Hackathon-Ready Government Portal</center>",
    unsafe_allow_html=True
)
