import os
import json
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

st.title("🤖 AI - ChatBot")

prompt1 = st.text_input("Ask anything.....")

def handle_tool_response(response_content):
    """
    Handles the tool response if the model's output includes tool calls.
    """
    try:
        # Attempt to find tool call in the response
        if "<tool_call>" in response_content and "</tool_call>" in response_content:
            start = response_content.index("<tool_call>") + len("<tool_call>")
            end = response_content.index("</tool_call>")
            tool_call = response_content[start:end].strip()

            # Parse the tool call content
            tool_call_data = json.loads(tool_call)
            tool_name = tool_call_data.get("name", "unknown tool")
            tool_arguments = tool_call_data.get("arguments", {})

            # Example tool handling logic
            if tool_name == "date":
                return f"(Tool) Today's date is: {tool_arguments.get('date', 'N/A')}"
            else:
                return f"(Tool) Tool call detected for: {tool_name} with arguments {tool_arguments}"

    except Exception as e:
        return f"(Error) Could not parse tool call: {str(e)}"

    return response_content

if prompt1:
    response = llm.invoke(prompt1)
    processed_response = handle_tool_response(response.content)
    st.session_state.chat_history.append({"question": prompt1, "response": processed_response})

for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['question']}")
    st.write(f"**Bot:** {chat['response']}")
