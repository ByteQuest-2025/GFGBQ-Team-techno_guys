import streamlit as st
import joblib
from utils import get_priority, get_department

# Load trained model
model = joblib.load("model/classifier.pkl")

st.title("AI-Powered Grievance Redressal System")

st.write("Enter a citizen complaint below:")

complaint = st.text_area("Complaint")

if st.button("Analyze Complaint"):
    if complaint.strip() == "":
        st.warning("Please enter a complaint.")
    else:
        category = model.predict([complaint])[0]
        priority = get_priority(complaint)
        department = get_department(category)

        st.subheader("Analysis Result")
        st.write(f"**Category:** {category}")
        st.write(f"**Priority:** {priority}")
        st.write(f"**Assigned Department:** {department}")
