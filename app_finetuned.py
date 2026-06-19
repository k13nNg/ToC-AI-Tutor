import streamlit as st

st.set_page_config(page_title="ToC Tutor (Fine-tuned)", page_icon="🧠")
st.title("🧠 Theory of Computation Tutor (Fine-tuned Gemma 3 1B)")

# ---------------------------------------------------------------------------
# Load model once — this takes ~10s and significant RAM
# ---------------------------------------------------------------------------
@st.cache_resource
def load_model():
    from retrieve.llm_finetuned import ask_finetuned
    return ask_finetuned

ask_finetuned = load_model()

# ---------------------------------------------------------------------------
# Session state (chat memory)
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Render chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------------------------------------------------------------------
# User input
# ---------------------------------------------------------------------------
user_input = st.chat_input("Ask something about Theory of Computation...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_finetuned(user_input, st.session_state.messages)
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
