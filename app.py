import sys
import os
from pathlib import Path

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

sys.path.insert(0, str(Path(__file__).resolve().parent / "RAG"))

import streamlit as st
from RAG.retrieve.llm_groq import ask_llm

st.set_page_config(page_title="Decidr", page_icon="🧠")

st.markdown("""
<style>
/* Hide Streamlit's own top header bar */
header[data-testid="stHeader"] {
    display: none;
}

/* Anchor links gone */
h1 a, h2 a, h3 a,
h1 a.anchor, h2 a.anchor, h3 a.anchor {
    display: none !important;
}

/* Floating title bar */
.floating-title {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background-color: #0e1117;
    padding: 0.4rem 2rem;
    border-bottom: 1px solid #2a2a2a;
}

.floating-title h1 {
    margin: 0;
    font-size: 1.8rem;
    color: white;
    text-align: center;
}

/* Push content down to clear the fixed bar */
.block-container {
    padding-top: 5rem !important;
}

/* Suggestion chips */
div[data-testid="stHorizontalBlock"] button {
    border: 1px solid #444 !important;
    border-radius: 1rem !important;
    background-color: transparent !important;
    font-size: 0.85rem !important;
    padding: 0.3rem 0.8rem !important;
    white-space: normal !important;
    width: 100% !important;
    height: 4rem !important;
    text-align: left !important;
}
</style>

<div class="floating-title">
    <h1>🧠 Decidr</h1>
</div>
""", unsafe_allow_html=True)

SUGGESTIONS = [
    "What is a DFA?",
    "Explain the Pumping Lemma for Regular Languages",
    "What is a Turing machine?",
    "What does it mean for a language to be decidable?",
    "What is the difference between NFA and DFA?",
    "What is a PDA?",
]

# ----------------------------
# Session state
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggestion_input" not in st.session_state:
    st.session_state.suggestion_input = None

# ----------------------------
# Render chat history
# ----------------------------
for msg in st.session_state.messages:
    icon = "🧠" if msg["role"] == "assistant" else "🧐"
    with st.chat_message(msg["role"], avatar=icon):
        st.markdown(msg["content"])

# ----------------------------
# User input
# ----------------------------
user_input = st.chat_input("Ask Decidr something about Theory of Computation...")

if st.session_state.suggestion_input:
    user_input = st.session_state.suggestion_input
    st.session_state.suggestion_input = None

# ----------------------------
# Suggestion chips (only when chat is empty)
# ----------------------------
if not st.session_state.messages and not st.session_state.suggestion_input and not user_input:
    cols = st.columns(3)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 3].button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            st.session_state.suggestion_input = suggestion
            st.rerun()

if user_input:
    with st.chat_message("user", avatar="🧐"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🧠"):
        placeholder = st.empty()
        tokens = []
        generator = ask_llm(user_input, st.session_state.messages)

        # Show spinner until first token arrives
        with st.spinner("Thinking..."):
            first = next(generator, None)

        if first:
            tokens.append(first)
            placeholder.markdown(first + "▌")
            for token in generator:
                tokens.append(token)
                placeholder.markdown("".join(tokens) + "▌")

        answer = "".join(tokens)
        placeholder.markdown(answer)

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": answer})
