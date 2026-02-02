import streamlit as st

# navigation set up
pg = st.navigation([
    st.Page("HW/HW1.py", title="Homework 1: File Summarizer"),
    st.Page("HW/HW2.py", title="Homework 2: URL Summarizer")
])

# shared page configuration
st.set_page_config(page_title="HW Manager", layout="wide")

# title
st.title("HW Manager")
st.write("Use the sidebar to navigate between your assignments.")

# 2. Run the navigation
pg.run()
