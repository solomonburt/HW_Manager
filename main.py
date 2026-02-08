import streamlit as st

# Setup navigation pages
pg = st.navigation([
    st.Page("HW/HW1.py", title="Homework 1: File Summarizer"),
    st.Page("HW/HW2.py", title="Homework 2: URL Summarizer"),
    st.Page("HW/HW3.py", title="Homework 3: URL Chatbot") # Added HW3
])

# Shared page configuration
st.set_page_config(page_title="HW Manager", layout="wide")

# App title
st.title("HW Manager")
st.write("Use the sidebar to navigate between your assignments.")

# Run navigation
pg.run()
