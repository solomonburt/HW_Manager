import requests
from bs4 import BeautifulSoup
import streamlit as st

def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # exeception for errors
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

# UI for URL Input
target_url = st.text_input("Enter a Web page URL")
