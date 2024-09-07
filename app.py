import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Me!",
    page_icon=":brain:",
    layout="centered",
)

# Get API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is not set. Please configure your environment variables.")
    st.stop()

llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-groq-70b-8192-tool-use-preview")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 AI - Copilot")

prompt1 = st.text_input("Ask anything.....")

if prompt1:
    response = llm.invoke(prompt1)
    st.session_state.chat_history.append({"question": prompt1, "response": response.content})

for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['question']}")
    st.write(f"**Bot:** {chat['response']}")
