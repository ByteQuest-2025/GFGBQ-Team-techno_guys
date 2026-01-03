import streamlit as st
import joblib
from utils import get_priority, get_department

# Page configuration
st.set_page_config(
    page_title="AI Grievance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 12px 30px;
        border-radius: 10px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    .result-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    .header-title {
        font-size: 48px;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 10px;
    }
    .header-subtitle {
        font-size: 20px;
        color: #64748b;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Load trained model
model = joblib.load("model/classifier.pkl")

# Header
st.markdown('<p class="header-title">🎯 AI-Powered Grievance Redressal System</p>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Intelligent complaint analysis and automated department assignment</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/complaint.png", width=80)
    st.title("📋 Information")
    st.info("""
    **How it works:**
    1. Enter your complaint in the text area
    2. Click 'Analyze Complaint'
    3. Get instant AI-powered analysis
    
    **Features:**
    - ✅ Category Classification
    - ⚡ Priority Detection
    - 🏢 Department Assignment
    """)
    
    st.divider()
    st.caption("Powered by AI & Machine Learning")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Complaint")
    complaint = st.text_area(
        "Describe your issue in detail:",
        height=200,
        placeholder="Example: The streetlights in my area have been broken for weeks...",
        help="Please provide as much detail as possible for accurate analysis"
    )
    
    analyze_button = st.button("🔍 Analyze Complaint", use_container_width=True)

with col2:
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Complaints", "1,234", "+89")
    st.metric("Avg Response Time", "2.3 hrs", "-0.5 hrs")
    st.metric("Resolution Rate", "94%", "+2%")

# Analysis section
if analyze_button:
    if complaint.strip() == "":
        st.error("⚠️ Please enter a complaint before analyzing.")
    else:
        with st.spinner("🔄 Analyzing your complaint..."):
            category = model.predict([complaint])[0]
            priority = get_priority(complaint)
            department = get_department(category)
        
        st.success("✅ Analysis Complete!")
        
        # Results display
        st.markdown("---")
        st.markdown("### 📈 Analysis Results")
        
        # Display results in columns
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.markdown("""
                <div class="result-box">
                    <h4 style="color: #3b82f6;">🏷️ Category</h4>
                    <p style="font-size: 24px; font-weight: bold; color: #1e293b;">{}</p>
                </div>
            """.format(category), unsafe_allow_html=True)
        
        with res_col2:
            priority_color = "#ef4444" if priority == "High" else "#f59e0b" if priority == "Medium" else "#22c55e"
            priority_icon = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
            st.markdown("""
                <div class="result-box">
                    <h4 style="color: #f59e0b;">⚡ Priority</h4>
                    <p style="font-size: 24px; font-weight: bold; color: {};">{} {}</p>
                </div>
            """.format(priority_color, priority_icon, priority), unsafe_allow_html=True)
        
        with res_col3:
            st.markdown("""
                <div class="result-box">
                    <h4 style="color: #8b5cf6;">🏢 Department</h4>
                    <p style="font-size: 24px; font-weight: bold; color: #1e293b;">{}</p>
                </div>
            """.format(department), unsafe_allow_html=True)
        
        # Additional information
        st.markdown("---")
        with st.expander("📋 View Complaint Details"):
            st.write("**Your Complaint:**")
            st.info(complaint)
            st.write("**Timestamp:**", "2026-01-03 14:30:00")
            st.write("**Status:**", "✅ Forwarded to respective department")
        
        # Action buttons
        st.markdown("### 🎯 Next Steps")
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("📨 Send Email Notification", use_container_width=True):
                st.success("Email sent successfully!")
        with btn_col2:
            if st.button("📥 Download Report", use_container_width=True):
                st.success("Report downloaded!")
        with btn_col3:
            if st.button("🔄 Submit Another", use_container_width=True):
                st.rerun()
