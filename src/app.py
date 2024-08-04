import ollama
import streamlit as st
from tts_service import TTSService
import os
import time
import base64

# Initialize Streamlit app
st.title("Personal GPT with Text-to-Speech")

# Initialize TTS model (do this only once)
@st.cache_resource
def load_tts_service():
    return TTSService()

tts_service = load_tts_service()

# Set default session state values
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "model" not in st.session_state:
    st.session_state["model"] = ""
if "stop_generation" not in st.session_state:
    st.session_state["stop_generation"] = False
if "archived_chats" not in st.session_state:
    st.session_state["archived_chats"] = {}
if "load_chat" not in st.session_state:
    st.session_state["load_chat"] = False
if "show_save_input" not in st.session_state:
    st.session_state["show_save_input"] = False
if "chat_to_load" not in st.session_state:
    st.session_state["chat_to_load"] = None

# Initialize Models
if not st.session_state["model"]:
    try:
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose Model", models)
    except Exception as e:
        st.error(f"Failed to load models: {e}. Please check your internet connection or model availability.")

# Function to save current chat
def save_chat(chat_name):
    st.session_state["archived_chats"][chat_name] = st.session_state["messages"].copy()
    st.success(f"Chat '{chat_name}' saved!")
    st.session_state["show_save_input"] = False

# Function to start a new chat
def start_new_chat():
    st.session_state["messages"] = []
    st.success("Started new chat.")

# Function to load a chat
def load_chat(chat_name):
    st.session_state["chat_to_load"] = chat_name
    st.query_params.update({"chat": chat_name})

# Load chat from query params if set
query_params = st.query_params
if "chat" in query_params:
    chat_name = query_params["chat"]
    if isinstance(chat_name, list):
        chat_name = chat_name[0]
    if chat_name in st.session_state["archived_chats"]:
        st.session_state["messages"] = st.session_state["archived_chats"][chat_name]
        st.session_state["chat_to_load"] = None
        st.query_params.clear()  # Clear query params after loading

# Model response generator
def model_res_gen():
    try:
        stream = ollama.chat(
            model=st.session_state["model"],
            messages=st.session_state["messages"],
            stream=True
        )
        for chunk in stream:
            if st.session_state["stop_generation"]:
                break
            yield chunk["message"]["content"]
    except Exception as e:
        st.error(f"Error generating model response: {e}")

# Function to display chat messages
def display_chat_messages():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "audio" in message:
                audio_bytes = base64.b64decode(message["audio"])
                st.audio(audio_bytes, format='audio/mp3')

# Function to display archived chats in the sidebar
def display_archived_chats():
    with st.sidebar:
        st.header("Chat History (Double-click to load)")
        for chat_name in st.session_state["archived_chats"]:
            if st.button(f"Load Chat: {chat_name}", key=f"load_{chat_name}"):
                load_chat(chat_name)

# Function to handle stop button
def stop_generation():
    st.session_state["stop_generation"] = True

display_chat_messages()

# Handle new chat input
col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.chat_input("What's up?")
with col2:
    stop_button_pressed = st.button("Stop Generation", on_click=stop_generation)

if prompt:
    st.session_state["stop_generation"] = False
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in model_res_gen():
            if st.session_state["stop_generation"]:
                break
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.1)  # Allow Streamlit to handle UI events
        message_placeholder.markdown(full_response)
        st.session_state["messages"].append({"role": "assistant", "content": full_response})

        # Generate TTS for assistant's response and store it
        audio_buffer = tts_service.text_to_speech(full_response)
        if audio_buffer:
            audio_bytes = audio_buffer.read()
            st.session_state["messages"][-1]["audio"] = base64.b64encode(audio_bytes).decode('utf-8')
            st.audio(audio_bytes, format='audio/mp3')

# Add buttons for saving and starting a new chat
col1, col2 = st.columns(2)
with col1:
    if st.button("Save Chat"):
        st.session_state["show_save_input"] = True
with col2:
    if st.button("New Chat"):
        start_new_chat()

# Input field to enter the chat name for saving, shown only when Save Chat is clicked
if st.session_state["show_save_input"]:
    chat_name = st.text_input("Enter chat name to save:")
    if st.button("Confirm Save") and chat_name:
        save_chat(chat_name)

display_archived_chats()
