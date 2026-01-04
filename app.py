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

/* Larger font sizes globally */
.stMarkdown {
    font-size: 17px !important;
}

h1 {
    font-size: 2.5rem !important;
}

h2 {
    font-size: 2rem !important;
}

h3 {
    font-size: 1.6rem !important;
}

/* Input fields - larger text */
.stTextInput input, .stTextArea textarea {
    font-size: 16px !important;
}

/* Buttons - larger text */
.stButton button {
    font-size: 17px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
}

/* Metrics - larger text */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: 1.1rem !important;
}

/* Header */
.gov-header {
    width: 100%;
    background: linear-gradient(90deg, #FF6B35, #F7931E);
    color: white;
    text-align: center;
    padding: 24px 10px;
    font-size: 28px;
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
    font-size: 18px !important;
    font-weight: 600;
    padding: 14px 0;
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

/* Success/Error messages - larger */
.stSuccess, .stError, .stWarning, .stInfo {
    font-size: 16px !important;
}

/* Dataframe text */
.stDataFrame {
    font-size: 15px !important;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="gov-header">
🇮🇳 Government of India | AI-Powered Grievance Redressal System
</div>
""", unsafe_allow_html=True)

# ================= DATABASE & MODEL =================
db = GrievanceDatabase()

@st.cache_resource
def load_model():
    path = "model/classifier.pkl"
    return joblib.load(path) if os.path.exists(path) else None

model = load_model()

def predict_category(text):
    if model:
        try:
            return model.predict([text])[0]
        except:
            return "Administrative"
    return "Administrative"

# ================= TABS =================
tabs = st.tabs([
    "🏠 Submit Complaint",
    "📊 Dashboard",
    "🔍 Track Complaint",
    "⚙️ Admin Panel"
])

# ================= TAB 1: SUBMIT COMPLAINT =================
with tabs[0]:
    st.markdown("## Register New Grievance")
    
    # Help section
    with st.expander("ℹ️ How to Submit a Complaint"):
        st.markdown("""
        **Steps to register your grievance:**
        1. Fill in your personal details (Name, Email, Phone)
        2. Describe your complaint clearly and in detail
        3. Click 'Submit Official Complaint'
        4. Save your Ticket ID for tracking
        5. Download the PDF receipt for your records
        
        **Tips for better processing:**
        - Be specific about the issue and location
        - Mention urgency if it's a critical issue
        - Include relevant dates and times
        """)

    with st.form("grievance_form"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", help="Enter your full legal name")
            email = st.text_input("Email Address *", help="We'll send updates to this email")
            phone = st.text_input("Phone Number", help="Optional - for urgent updates")

        with col2:
            complaint_text = st.text_area(
                "Complaint Details *",
                height=160,
                placeholder="Describe your grievance clearly...",
                help="Provide detailed information about your complaint"
            )

        st.markdown("</div>", unsafe_allow_html=True)
        
        # Anonymous submission option
        anonymous = st.checkbox("Submit anonymously (name will be hidden from public view)")
        
        submit = st.form_submit_button("🚀 Submit Official Complaint", use_container_width=True)

    if submit:
        if not name or not email or not complaint_text:
            st.error("⚠️ Please fill all required fields")
        else:
            with st.spinner("🤖 AI is analyzing your complaint..."):
                category = predict_category(complaint_text)
                priority = get_priority(complaint_text)
                department = get_department(category)
                sentiment = get_sentiment(complaint_text)
                keywords = extract_keywords(complaint_text)
                resolution = estimate_resolution_time(category, priority)
                ticket_id = generate_ticket_id()

                submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Handle anonymous submission
                display_name = "Anonymous" if anonymous else name

                complaint_data = {
                    "ticket_id": ticket_id,
                    "name": display_name,
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

            st.success("✅ Complaint registered successfully!")
            st.markdown(f"### 🎫 Your Ticket ID: `{ticket_id}`")
            st.balloons()
            
            # Display AI analysis results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📋 Category", category)
                st.metric("⚡ Priority", priority)
            with col2:
                st.metric("🏢 Department", department)
                st.metric("⏰ Est. Resolution", resolution)
            with col3:
                st.metric("💭 Sentiment", sentiment["label"])
                st.metric("🔑 Keywords", len(keywords))
            
            st.info(f"🔑 **Keywords identified:** {', '.join(keywords)}")

            pdf_path = generate_pdf_report(
                ticket_id,
                {
                    "Name": display_name,
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
                    "📄 Download Official Receipt (PDF)",
                    data=pdf,
                    file_name=f"Grievance_{ticket_id}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            st.warning("⚠️ **Important:** Save your Ticket ID to track your complaint status")

# ================= TAB 2: DASHBOARD =================
with tabs[1]:
    st.markdown("## 📊 Analytics Dashboard")
    
    data = db.get_all_complaints()
    if data:
        df = pd.DataFrame(data)
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Total Complaints", len(df))
        with col2:
            pending_count = (df["status"] == "Pending").sum()
            st.metric("🟡 Pending", pending_count, delta="Needs Action" if pending_count > 0 else "All Clear")
        with col3:
            in_progress = (df["status"] == "In Progress").sum()
            st.metric("🔵 In Progress", in_progress)
        with col4:
            resolved = (df["status"] == "Resolved").sum()
            resolution_pct = (resolved/len(df)*100) if len(df) > 0 else 0
            st.metric("✅ Resolved", resolved, delta=f"{resolution_pct:.0f}% Rate")
        
        st.markdown("---")
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            critical = (df["priority"] == "Critical").sum()
            st.metric("🚨 Critical Priority", critical, delta="⚠️ Urgent" if critical > 0 else None)
        with col2:
            avg_sentiment = df["sentiment_score"].mean() if "sentiment_score" in df.columns else 0
            sentiment_label = "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral"
            st.metric("💭 Avg Sentiment", sentiment_label, delta=f"{avg_sentiment:.2f}")
        with col3:
            today_complaints = len(df[df["submitted_at"].str.contains(datetime.now().strftime("%Y-%m-%d"))])
            st.metric("📅 Today's Complaints", today_complaints)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏢 Complaints by Department")
            st.bar_chart(df["department"].value_counts())
            
            st.markdown("### ⚡ Priority Distribution")
            priority_data = df["priority"].value_counts()
            st.bar_chart(priority_data)
        
        with col2:
            st.markdown("### 📋 Complaints by Category")
            st.bar_chart(df["category"].value_counts())
            
            st.markdown("### 📊 Status Overview")
            status_data = df["status"].value_counts()
            st.bar_chart(status_data)
        
        st.markdown("---")
        st.markdown("### 📌 Recent Complaints")
        recent_df = df[["ticket_id", "name", "category", "priority", "status", "submitted_at"]].tail(10)
        st.dataframe(recent_df, use_container_width=True, height=350)
        
        # Quick stats
        st.markdown("### 📈 Quick Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"**Most Common Category:**\n{df['category'].mode()[0]}")
        with col2:
            st.info(f"**Most Assigned Dept:**\n{df['department'].mode()[0]}")
        with col3:
            high_priority = ((df["priority"] == "High").sum() + (df["priority"] == "Critical").sum())
            st.warning(f"**High Priority Issues:**\n{high_priority}")
        with col4:
            st.success(f"**Resolution Rate:**\n{resolution_pct:.1f}%")
        
    else:
        st.info("📭 No complaints registered yet. Submit the first complaint!")

# ================= TAB 3: TRACK COMPLAINT =================
with tabs[2]:
    st.markdown("## 🔍 Track Your Complaint")
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    ticket = st.text_input("Enter Your Ticket ID", placeholder="GRV-20260104-XXXX")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        search_btn = st.button("🔎 Track Complaint", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_btn:
        if not ticket:
            st.warning("Please enter a ticket ID")
        else:
            res = db.get_complaint_by_ticket(ticket)
            if res:
                st.success("✅ Complaint Found!")
                
                # Display complaint details in organized format
                st.markdown("### Complaint Details")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**👤 Name:** {res['name']}")
                    st.markdown(f"**📧 Email:** {res['email']}")
                    st.markdown(f"**📱 Phone:** {res['phone']}")
                    st.markdown(f"**📋 Category:** {res['category']}")
                    st.markdown(f"**🏢 Department:** {res['department']}")
                
                with col2:
                    st.markdown(f"**⚡ Priority:** {res['priority']}")
                    st.markdown(f"**📊 Status:** {res['status']}")
                    st.markdown(f"**⏰ Resolution Time:** {res['resolution_time']}")
                    st.markdown(f"**📅 Submitted:** {res['submitted_at']}")
                
                st.markdown("---")
                st.markdown("### Complaint Description")
                st.info(res['complaint_text'])
                
                # Status timeline
                st.markdown("### Status Timeline")
                if res['status'] == "Pending":
                    st.progress(0.33)
                    st.caption("🟡 Pending → ⚪ In Progress → ⚪ Resolved")
                elif res['status'] == "In Progress":
                    st.progress(0.66)
                    st.caption("✅ Pending → 🟡 In Progress → ⚪ Resolved")
                else:
                    st.progress(1.0)
                    st.caption("✅ Pending → ✅ In Progress → ✅ Resolved")
            else:
                st.error("❌ Ticket ID not found. Please check and try again.")

# ================= TAB 4: ADMIN PANEL =================
with tabs[3]:
    st.markdown("## ⚙️ Admin Control Panel")
    
    # Initialize session state
    if "admin" not in st.session_state:
        st.session_state.admin = False

    if not st.session_state.admin:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🔒 Authentication Required")
        st.info("Please enter admin credentials to access the control panel")
        
        pwd = st.text_input("Admin Password", type="password", key="admin_pwd")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔓 Login", use_container_width=True):
                if pwd == "admin123":
                    st.session_state.admin = True
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        st.caption("**Default Password:** admin123")
        
    else:
        # Admin Dashboard
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.admin = False
                st.rerun()
        
        st.markdown("---")
        
        # Get all complaints
        complaints = db.get_all_complaints()
        
        if complaints:
            df = pd.DataFrame(complaints)
            
            # Admin Metrics
            st.markdown("### 📈 Quick Statistics")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total", len(df))
            with col2:
                critical = (df["priority"] == "Critical").sum()
                st.metric("Critical", critical, delta="High Priority" if critical > 0 else None)
            with col3:
                st.metric("High", (df["priority"] == "High").sum())
            with col4:
                pending = (df["status"] == "Pending").sum()
                st.metric("Pending", pending, delta="Needs Action" if pending > 0 else None)
            with col5:
                resolved = (df["status"] == "Resolved").sum()
                resolution_rate = f"{(resolved/len(df)*100):.1f}%"
                st.metric("Resolved", f"{resolved} ({resolution_rate})")
            
            st.markdown("---")
            
            # Filters
            st.markdown("### 🔍 Filter Complaints")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_status = st.selectbox(
                    "Filter by Status",
                    ["All", "Pending", "In Progress", "Resolved"]
                )
            
            with col2:
                filter_priority = st.selectbox(
                    "Filter by Priority",
                    ["All", "Critical", "High", "Medium", "Low"]
                )
            
            with col3:
                filter_category = st.selectbox(
                    "Filter by Category",
                    ["All"] + list(df["category"].unique())
                )
            
            # Apply filters
            filtered_df = df.copy()
            if filter_status != "All":
                filtered_df = filtered_df[filtered_df["status"] == filter_status]
            if filter_priority != "All":
                filtered_df = filtered_df[filtered_df["priority"] == filter_priority]
            if filter_category != "All":
                filtered_df = filtered_df[filtered_df["category"] == filter_category]
            
            st.markdown(f"### 📋 All Complaints ({len(filtered_df)} records)")
            
            # Display complaints table
            st.dataframe(
                filtered_df[[
                    "ticket_id", "name", "email", "category", "priority", 
                    "status", "department", "submitted_at"
                ]],
                use_container_width=True,
                height=400
            )
            
            st.markdown("---")
            
            # Update Status Section
            st.markdown("### ✏️ Update Complaint Status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                update_ticket = st.text_input(
                    "Ticket ID to Update",
                    placeholder="GRV-20260104-XXXX"
                )
            
            with col2:
                new_status = st.selectbox(
                    "New Status",
                    ["Pending", "In Progress", "Resolved"],
                    index=1
                )
            
            with col3:
                st.write("")  # Spacing
                st.write("")  # Spacing
                if st.button("🔄 Update Status", use_container_width=True):
                    if update_ticket:
                        if db.update_complaint_status(update_ticket, new_status):
                            st.success(f"✅ Status updated to '{new_status}' for ticket {update_ticket}")
                            st.rerun()
                        else:
                            st.error("❌ Invalid Ticket ID")
                    else:
                        st.warning("Please enter a Ticket ID")
            
            st.markdown("---")
            
            # Bulk Actions
            st.markdown("### 🔧 Bulk Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Export All Data (CSV)", use_container_width=True):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        file_name=f"grievances_export_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                st.info(f"💾 Database: {len(df)} total records")
            
        else:
            st.info("No complaints in the system yet")

# ================= FOOTER =================
st.markdown("<hr><center>🇮🇳 National AI Redressal Framework | 2026</center>", unsafe_allow_html=True)
