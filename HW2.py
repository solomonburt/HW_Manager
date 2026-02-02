import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import google.generativeai as genai

# Function to read content from a URL
def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

# SIDEBAR
with st.sidebar:
    st.header("Settings")
    
    #summary chooser
    summary_type = st.selectbox(
        "Select the type of summary", 
        ["Summarize in 5 bullet points", "Summarize in 3 paragraphs", "Summarize for a 5th grader"]
    )
    # language chooser
    output_lang = st.selectbox(
        "Select the language to output", 
        ["English", "French", "Spanish", "German"]
    )
    
    # llm chooser
    llm_provider = st.radio("Select LLM Provider", ["OpenAI", "Gemini"])
    
    # advanced checkbox
    use_advanced = st.checkbox("Use advanced model")

# main ui
st.title("URL Summarizer")
target_url = st.text_input("Enter a Web page URL")
if target_url:
    with st.spinner(f"Generating {output_lang} summary using {llm_provider}..."):
        # Fetch text content
        web_text = read_url_content(target_url)
        
        if web_text:
            # prompt update for correctness
            prompt = f"Using the following text: '{web_text}', provide a summary in {output_lang}. The style should be: {summary_type}."
            
            summary = ""
            
            # Switch logic based llm
            try:
                if llm_provider == "OpenAI":
                    # Determine model tier
                    model_name = "gpt-4o" if use_advanced else "gpt-3.5-turbo"
                    
                   # secrets.toml for keys
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    summary = response.choices[0].message.content

                elif llm_provider == "Gemini":
                    model_name = "gemini-1.5-pro" if use_advanced else "gemini-1.5-flash"
                    
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    summary = response.text

                # summary out[ut
                st.subheader(f"Summary ({llm_provider})")
                st.write(summary)
                
            except Exception as e:
                st.error(f"An error occurred with the {llm_provider} API: {e}")
