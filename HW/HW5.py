import streamlit as st
import os
import chromadb
from openai import OpenAI

# setup path
db_path = "chroma_db_storage"
collection_name = "su_orgs"

def get_relevant_club_info(query):
    client = chromadb.PersistentClient(path=db_path)
    # check for collection
    try:
        collection = client.get_collection(name=collection_name)
    except:
        return "ERROR: Collection not found. Please run the data ingestion script first."
        
    collection = client.get_or_create_collection(name=collection_name)
    
    # vector search
    results = collection.query(query_texts=[query], n_results=3)

    # Check if documents list is empty
    if not results['documents'] or not results['documents'][0]:
        return "No relevant documents found."
        
    # Flatten documents into string
    context = "\n\n".join(results['documents'][0])
    return context

st.title("HW5: Intelligent Club Chatbot")
st.write("I have short-term memory and search through student organization docs!")

# Initialize Chat History 
if "hw5_messages" not in st.session_state:
    st.session_state.hw5_messages = []

# display chat history
for message in st.session_state.hw5_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What would you like to know about SU clubs?"):
    # add user message to history
    st.session_state.hw5_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # retrieve relevant info
    retrieved_info = get_relevant_club_info(prompt)

    # Invoke the LLM
    ai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # Construct message list with System Prompt + Short-term memory (last 5 exchanges)
    messages_to_send = [
        {
            "role": "system", 
            "content": (
            "You are a helpful assistant. Use ONLY the following context to answer the user's question. "
            "If the information is not in the context, say 'I don't know based on the documents provided.' "
            f"Context: {retrieved_info}"
        }
    ]
    messages_to_send.extend(st.session_state.hw5_messages[-10:]) 

    # display response
    with st.chat_message("assistant"):
        stream = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages_to_send,
            stream=True,
        )
        response = st.write_stream(stream)
    
    # add assistant response to history
    st.session_state.hw5_messages.append({"role": "assistant", "content": response})
