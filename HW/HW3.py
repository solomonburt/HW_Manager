import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import google.generativeai as genai

# Page title and description
st.title("HW3: URL Chatbot")
st.write("Chat with URLs using a 6-message buffer.")

# Sidebar configurations
with st.sidebar:
    st.header("Settings")
    # URL inputs
    url1 = st.text_input("Enter URL 1")
    url2 = st.text_input("Enter URL 2")
    
    # Model selection
    model_choice = st.selectbox(
        "Select Premium Model",
        options=["gpt-4o", "gemini-1.5-pro"]
    )

# Function from HW2
def read_url_content(url):
    if not url: return ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except: return ""

# Initialize chat history
if "messages" not in st.session_state:
    context = read_url_content(url1) + "\n" + read_url_content(url2)
    st.session_state.messages = [
        {"role": "system", "content": f"Use this context: {context}"}
    ]

# Display history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User interaction
if prompt := st.chat_input("Ask about the URLs:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6-message memory buffer
    sys_prompt = st.session_state.messages[0]
    # Keep last 6 messages
    buffer = [m for m in st.session_state.messages[-6:] if m["role"] != "system"]
    msgs_to_send = [sys_prompt] + buffer

    with st.chat_message("assistant"):
        if "gpt" in model_choice:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            stream = client.chat.completions.create(
                model=model_choice, messages=msgs_to_send, stream=True
            )
            response = st.write_stream(stream)
        else:
            # Gemini provider logic
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel(model_choice)
            # Reformat for Gemini
            gemini_history = [{"role": "user" if m["role"]=="user" else "model", 
                               "parts": [m["content"]]} for m in msgs_to_send]
            response = model.generate_content(gemini_history).text
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
