from google import genai
from retriever import notes_search, exercises_search
import streamlit as st
import ollama

system_instruction = ""

with open("prompt.txt", "r") as f:
    system_instruction = f.read()

st.title("Theory of Computation Tutor")

# client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
# 1. Initialize the client only if it doesn't exist
if "client" not in st.session_state:
    st.session_state["client"] = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Assign the persistent client object to the local variable
client = st.session_state["client"]

if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Only create the chat_session object if it doesn't exist yet
if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = client.chats.create(
        model=st.session_state["gemini_model"], # Use the model from session state
        config={"system_instruction": system_instruction}
    )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    query_embeddings = ollama.embed("embeddinggemma", query)

    retrieved_context = f"\n\nNotes:\n\n{
        notes_search(query, query_embeddings)
    }\n\nExercises:\n\n{
        exercises_search(query_embeddings)
    }"

    prompt = f"""
    ### Retrieved context:
    {retrieved_context}

    ### User Query:
    {query}
    """

    with st.chat_message("assistant"):
        chat_session = st.session_state["chat_session"]

        # 1. Use the correct streaming method
        stream = chat_session.send_message_stream(prompt)

        # 2. Set up a placeholder and response variables
        placeholder = st.empty()
        full_response = ""

        # 3. Iterate over the stream and update the placeholder
        for chunk in stream:
            # The chunk contains the text part
            if chunk.text:
                full_response += chunk.text
                # Write the accumulated response to the placeholder
                placeholder.markdown(full_response + "▌") # Add a cursor (▌) for effect

        # 4. Write the final, complete response without the cursor
        placeholder.markdown(full_response)
        response = full_response # Capture the final response text
        # response = st.write_stream(stream.text)
    st.session_state.messages.append({"role": "assistant", "content": response})