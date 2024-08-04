# app.py

import ollama
import streamlit as st
from tts_service import TTSService

# Initialize Streamlit app
st.title("Personal GPT with Text-to-Speech")

# Initialize TTS model (do this only once)
@st.cache_resource
def load_tts_service():
    return TTSService()

tts_service = load_tts_service()

# Set default session state values
st.session_state.setdefault("messages", [])
st.session_state.setdefault("model", "")

# Initialize Models
if not st.session_state["model"]:
    try:
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose Model", models)
    except Exception as e:
        st.error(f"Failed to load models: {e}")

# Model response generator
def model_res_gen():
    try:
        stream = ollama.chat(
            model=st.session_state["model"],
            messages=st.session_state["messages"],
            stream=True
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except Exception as e:
        st.error(f"Error generating model response: {e}")

# Function to display chat messages
def display_chat_messages():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

display_chat_messages()

# Handle new chat input
if prompt := st.chat_input("What's up?"):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in model_res_gen():
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
        
        # Add TTS button for assistant's response
        audio_buffer = tts_service.text_to_speech(full_response)
        if audio_buffer:
            st.audio(audio_buffer, format='audio/mp3')

# Function to save current chat
def save_chat():
    if "archived_chats" not in st.session_state:
        st.session_state["archived_chats"] = []
    st.session_state["archived_chats"].append(st.session_state["messages"])
    st.success("Chat saved!")

# Function to start a new chat
def start_new_chat():
    st.session_state["messages"] = []
    st.success("Started new chat.")

# Add buttons for saving and starting a new chat
if st.button("Save Chat"):
    save_chat()
if st.button("New Chat"):
    start_new_chat()

# Function to display archived chats in the sidebar
def display_archived_chats():
    with st.sidebar:
        st.header("Chat History")
        if "archived_chats" in st.session_state:
            for i, chat in enumerate(st.session_state["archived_chats"]):
                with st.expander(f"Chat {i + 1}"):
                    for message in chat:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])

display_archived_chats()