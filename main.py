import streamlit as st
# titling
st.set_page_config(page_title="HW Manager", layout="wide")
st.title("HW Manager")
st.write("Use the sidebar to navigate between your assignments.")

# define the pages
hw1 = st.Page("HW/HW1.py", title="Homework 1: File Summarizer")
hw2 = st.Page("HW/HW2.py", title="Homework 2: URL Summarizer")
hw3 = st.Page("HW/HW3.py", title="Homework 3: URL Chatbot")
hw4 = st.Page("HW/HW4.py", title="Homework 4: RAG Chatbot")
hw5 = st.Page("HW/HW5.py", title="Homework 5: Intelligent Chatbot") 
hw7 = st.Page("HW/HW7.py", title="Homework 7: News Chatbot", default=True) # Added for HW7
# navigation setup
pg = st.navigation([hw1, hw2, hw3, hw4, hw5, hw7])


pg.run()





