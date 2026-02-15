import streamlit as st
import os
from bs4 import BeautifulSoup
import chromadb 

def get_html_content(folder_path):
    documents = []
    for file in os.listdir(folder_path):
        if file.endswith(".html"):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                text = soup.get_text()
                # Chunking
                midpoint = len(text) // 2
                documents.append(text[:midpoint])
                documents.append(text[midpoint:])
    return documents

# only create DB if it doesn't exist
if "vector_db" not in st.session_state:
    # Build your DB here using the documents list
    st.session_state.vector_db = "Initialized" 
