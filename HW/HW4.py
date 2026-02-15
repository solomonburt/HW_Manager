import streamlit as st
import os
from bs4 import BeautifulSoup
import chromadb
from openai import OpenAI

# path setup
folder_path = os.path.join("HW", "su_orgs", "su_orgs")
db_path = "chroma_db_storage"

# chunking
def get_html_chunks(directory):
    documents = []
    metadatas = []
    ids = []
    
    # check if folder exists
    if not os.path.exists(directory):
        st.error(f"Folder not found at: {directory}")
        return documents, metadatas, ids

    for i, file in enumerate(os.listdir(directory)):
        if file.endswith(".html"):
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                text = soup.get_text().strip()
                
                # CHUNKING METHOD: Midpoint Split
                # I chose this simple method because the assignment requires 
                # creating exactly two mini-documents for each file.
                midpoint = len(text) // 2
                chunks = [text[:midpoint], text[midpoint:]]
                
                for j, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({"source": file})
                    ids.append(f"{file}_{j}")
                    
    return documents, metadatas, ids

# intiilize vector db
client = chromadb.PersistentClient(path=db_path)
collection = client.get_or_create_collection(name="su_orgs")

if collection.count() == 0:
    with st.spinner("Building vector database..."):
        docs, metas, doc_ids = get_html_chunks(folder_path)
        if docs:
            collection.add(documents=docs, metadatas=metas, ids=doc_ids)
            st.success("Vector DB created and documents loaded!")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input
if prompt := st.chat_input("Ask about SU student organizations:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG
    results = collection.query(query_texts=[prompt], n_results=2)
    retrieved_context = "\n\n".join(results['documents'][0])

    # generate response
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # system prompt
    messages_to_send = [
        {"role": "system", "content": f"Use this context to answer: {retrieved_context}"}
    ]
    
    # store 5 last interactions
    messages_to_send.extend(st.session_state.messages[-10:])

    with st.chat_message("assistant"):
        stream = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages_to_send,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
