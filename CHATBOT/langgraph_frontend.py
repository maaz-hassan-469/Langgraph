import streamlit as st
from Langgraph_backend import chat_bot,retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

st.set_page_config(page_title="LangGraph Chatbot", layout="wide", initial_sidebar_state="expanded")

#**********************utilities function*******************
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state["thread_id"]=thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"]=[]

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
def load_conversation(thread_id):
    state= chat_bot.get_state(config={"configurable":{"thread_id":thread_id}})
    return state.values.get("messages",[])


#**********************session setup***********************
# 1. Fix typo in session state initialization
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "thread_id" not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"]=retrieve_all_threads()

add_thread(st.session_state["thread_id"])

CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

#***********************sidebar setup**********************

st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My conversations')
for thread_id in st.session_state["chat_threads"]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"]=thread_id
        messages=load_conversation(thread_id)
        temp_messages=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role="user"
            else:
                role="assistant" 
            temp_messages.append({"role":role,"content":message.content})
        st.session_state["message_history"]=temp_messages

#************************Main UI***************************

# 2. Render previous messages with markdown formatting
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("type here")

if user_input:
    # Append and display user input
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream assistant response
    with st.chat_message("assistant"):
        # Helper generator to filter out empty content chunks
        def generate_stream():
            for message_chunk, metadata in chat_bot.stream(
                {"messages": [HumanMessage(content=user_input)]},  # Fix: Pass user_input here
                config=CONFIG,
                stream_mode="messages"
            ):
                if message_chunk.content:
                    yield message_chunk.content

        ai_message = st.write_stream(generate_stream)

    # Append complete assistant output to history
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})