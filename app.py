import streamlit as st
import joblib
from utils import get_priority, get_department

# Load trained model
model = joblib.load("model/classifier.pkl")

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
        padding: 2rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .result-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #333;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 0.5rem;
    }
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.write("""
    This AI-powered system automatically:
    - **Categorizes** citizen complaints
    - **Assigns priority** levels
    - **Routes** to appropriate departments
    """)
    
    st.divider()
    
    st.header("🎯 How to Use")
    st.write("""
    1. Enter your complaint in the text area
    2. Click "Analyze Complaint"
    3. View the AI-generated analysis
    """)
    
    st.divider()
    
    st.info("💡 Tip: Be specific in your complaint description for better results.")

# Main content
st.title("🎯 AI-Powered Grievance Redressal System")
st.markdown('<p class="subtitle">Smart complaint analysis and routing powered by machine learning</p>', unsafe_allow_html=True)

st.divider()

# Input section
st.markdown("### 📝 Submit Your Complaint")
complaint = st.text_area(
    "Complaint Details",
    placeholder="Describe your complaint here in detail...",
    height=150,
    help="Provide clear details about your issue for accurate analysis"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyze Complaint", use_container_width=True)

if analyze_button:
    if complaint.strip() == "":
        st.warning("⚠️ Please enter a complaint before analyzing.")
    else:
        with st.spinner("🤖 AI is analyzing your complaint..."):
            category = model.predict([complaint])[0]
            priority = get_priority(complaint)
            department = get_department(category)
        
        st.success("✅ Analysis Complete!")
        
        # Results section
        st.markdown("### 📊 Analysis Results")
        
        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">📂 Category</div>
                    <div class="metric-value">{}</div>
                </div>
            """.format(category), unsafe_allow_html=True)
        
        with col2:
            priority_color = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">⚡ Priority</div>
                    <div class="metric-value">{} {}</div>
                </div>
            """.format(priority_color, priority), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">🏢 Department</div>
                    <div class="metric-value">{}</div>
                </div>
            """.format(department), unsafe_allow_html=True)
        
        st.divider()
        
        # Additional info
        st.info(f"📌 Your complaint has been categorized as **{category}** and assigned to the **{department}** department with **{priority}** priority.")
