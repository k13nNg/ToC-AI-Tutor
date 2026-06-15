import streamlit as st
from retrieve.llm import ask_llm  # change this import
# from retrieve.llm_groq import ask_llm

st.set_page_config(page_title="ToC Tutor", page_icon="🧠")

st.title("🧠 Theory of Computation Tutor")

# ----------------------------
# Session state (chat memory)
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Render chat history
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------
# User input
# ----------------------------
user_input = st.chat_input("Ask something about Theory of Computation...")

if user_input:
    # 1. show user message immediately
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. generate response using your RAG pipeline
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_llm(user_input, st.session_state.messages)
            st.write(answer)

    # 3. store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })