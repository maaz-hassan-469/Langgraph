import streamlit as st
from langgraph_backend import chat_bot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "thread_1"}}

# 1. Fix typo in session state initialization
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

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