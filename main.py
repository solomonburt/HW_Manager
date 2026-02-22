import streamlit as st

# navigation set up
pg = st.navigation([
    st.Page("HW/HW1.py", title="Homework 1: File Summarizer"),
    st.Page("HW/HW2.py", title="Homework 2: URL Summarizer"),
    st.Page("HW/HW3.py", title="Homework 3: URL Chatbot"),
    st.Page("HW/HW4.py", title="Homework 4: RAG Chatbot"),
    st.Page("HW/HW5.py", title="Homework 5: Intelligent Chatbot") # Added for HW5
])

st.set_page_config(page_title="HW Manager", layout="wide")
st.title("HW Manager")
st.write("Use the sidebar to navigate between your assignments.")

pg.run()


