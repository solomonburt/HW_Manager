import streamlit as st
import chromadb
from openai import OpenAI
import os

# Configuration
DB_PATH = "news_db_storage"
COLLECTION_NAME = "news_monitor"

st.set_page_config(page_title="HW7: News Bot", layout="wide")

st.title("Client News Monitoring Bot")
st.write("Targeted RAG analysis for global law firm clients.")

# Initialize ChromaDB Client
@st.cache_resource
def get_db():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection(name=COLLECTION_NAME)

try:
    collection = get_db()
except Exception as e:
    st.error("Database not found. Please run ingest_news.py first.")
    st.stop()

def get_news_context(query, n_results=5):
    """Retrieves relevant articles from the Vector DB."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    formatted_context = ""
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        formatted_context += f"COMPANY: {meta['company_name']}\nDATE: {meta['Date']}\nCONTENT: {doc}\nURL: {meta['URL']}\n\n---\n"
    return formatted_context

def ask_llm(model, system_prompt, user_query, context):
    """Calls OpenAI API with specific model and context."""
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    full_prompt = f"Use the following news articles to answer the question.\n\nContext:\n{context}\n\nQuestion: {user_query}"
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ]
    )
    return response.choices[0].message.content

# Sidebar
with st.sidebar:
    st.header("Search Parameters")
    st.info("Try: 'Find the most interesting news' or 'Find news about Amazon'")

# Main Chat Interface
user_query = st.text_input("Enter your news query:", placeholder="e.g. Find news about JPMorgan")

if user_query:
    # Define the System Prompt
    system_persona = """You are a senior legal analyst for a global law firm. 
    Your goal is to monitor news for clients. 
    If the user asks for 'interesting' news, rank the articles by their potential legal risk, regulatory impact, or strategic importance.
    Always provide the 'Why' (context) for your ranking. 
    Be professional, concise, and cite the company names."""

    # Retrieve Context
    n = 10 if "interesting" in user_query.lower() else 5
    with st.spinner("Searching news database..."):
        context_data = get_news_context(user_query, n_results=n)

    # Dual Model Comparison
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 Low-Cost Model (gpt-4o-mini)")
        with st.spinner("Generating..."):
            ans_low = ask_llm("gpt-4o-mini", system_persona, user_query, context_data)
            st.markdown(ans_low)

    with col2:
        st.subheader("🧠 High-Cost Model (gpt-4o)")
        with st.spinner("Generating..."):
            ans_high = ask_llm("gpt-4o", system_persona, user_query, context_data)
            st.markdown(ans_high)

    # Debug/Source View
    with st.expander("Show Raw Data Sources"):
        st.text(context_data)
