import ollama
import streamlit as st
from tts_service import TTSService
import os
import time
import base64

# Initialize Streamlit app
st.set_page_config(page_title="UncensoredGPT with Text-to-Speech", layout="wide")
st.title("UncensoredGPT with Text-to-Speech")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f9;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 10px;
        background-color: #fff;
        border-top: 1px solid #ddd;
        z-index: 1000;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
    }
    .input-box {
        width: calc(25% - 160px);
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
    }
    .output-box {
        border: 1px solid #d3d3d3;
        padding: 10px;
        background-color: #e6f7e6;
        border-radius: 5px;
        margin-bottom: 10px;
        color: black;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .input-message {
        border: 1px solid #d3d3d3;
        padding: 10px;
        background-color: #ffe6e6;
        border-radius: 5px;
        margin-bottom: 10px;
        color: black;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stop-button {
        margin-top: 10px;
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stop-button:hover {
        background-color: #ff1f1f;
    }
    .send-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        margin-left: 10px;
    }
    .send-button:hover {
        background-color: #45a049;
    }
    .slider-container {
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .voice-dropdown {
        margin-top: 10px;
    }
    .chat-history {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

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
if "input_voice" not in st.session_state:
    st.session_state["input_voice"] = None
if "output_voice" not in st.session_state:
    st.session_state["output_voice"] = None
if "speech_rate" not in st.session_state:
    st.session_state["speech_rate"] = 130

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
        if message["role"] == "user":
            with st.chat_message(message["role"]):
                st.markdown(f'<div class="input-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            with st.chat_message(message["role"]):
                st.markdown(f'<div class="output-box">{message["content"]}</div>', unsafe_allow_html=True)
        if "audio" in message:
            audio_bytes = base64.b64decode(message["audio"])
            st.audio(audio_bytes, format='audio/mp3')

# Function to display archived chats in the sidebar
def display_archived_chats():
    with st.sidebar:
        st.header("Chat History (Double-click to load)")
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        for chat_name in st.session_state["archived_chats"]:
            if st.button(f"Load Chat: {chat_name}", key=f"load_{chat_name}"):
                load_chat(chat_name)
        st.markdown('</div>', unsafe_allow_html=True)

# Function to handle stop button
def stop_generation():
    st.session_state["stop_generation"] = True

display_chat_messages()

# Add voice selection dropdowns and speech rate slider
voices = tts_service.get_voices()
voice_options = {voice["name"]: voice["id"] for voice in voices}

input_voice = st.selectbox("Choose Input Voice", list(voice_options.keys()), key="input_voice_selection")
st.session_state["input_voice"] = voice_options[input_voice]

output_voice = st.selectbox("Choose Output Voice", list(voice_options.keys()), key="output_voice_selection")
st.session_state["output_voice"] = voice_options[output_voice]

speech_rate = st.slider("Speech Rate", min_value=50, max_value=200, value=st.session_state["speech_rate"], key="speech_rate_slider")
st.session_state["speech_rate"] = speech_rate
tts_service.set_rate(st.session_state["speech_rate"])

# Create a placeholder for the input box at the bottom
input_placeholder = st.empty()
with input_placeholder.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        prompt = st.text_input("What's up?", key="input_box", help="Type your message here and press Enter or click Send.", on_change=lambda: st.session_state.update({"enter_pressed": True}))
    with col2:
        if st.button("Send", key="send_button") or st.session_state.get('enter_pressed', False):
            st.session_state['enter_pressed'] = False
            st.session_state["stop_generation"] = False
            # Add user message to history
            st.session_state["messages"].append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(f'<div class="input-message">{prompt}</div>', unsafe_allow_html=True)

            # Generate TTS for user's input and store it
            user_audio_buffer = tts_service.text_to_speech(prompt, voice_id=st.session_state["input_voice"])
            if user_audio_buffer:
                user_audio_bytes = user_audio_buffer.read()
                st.session_state["messages"][-1]["audio"] = base64.b64encode(user_audio_bytes).decode('utf-8')
                st.audio(user_audio_bytes, format='audio/mp3')

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in model_res_gen():
                    if st.session_state["stop_generation"]:
                        break
                    full_response += chunk
                    message_placeholder.markdown(f'<div class="output-box">{full_response}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.1)  # Allow Streamlit to handle UI events
                message_placeholder.markdown(f'<div class="output-box">{full_response}</div>', unsafe_allow_html=True)
                st.session_state["messages"].append({"role": "assistant", "content": full_response})

                # Generate TTS for assistant's response and store it
                audio_buffer = tts_service.text_to_speech(full_response, voice_id=st.session_state["output_voice"])
                if audio_buffer:
                    audio_bytes = audio_buffer.read()
                    st.session_state["messages"][-1]["audio"] = base64.b64encode(audio_bytes).decode('utf-8')
                    st.audio(audio_bytes, format='audio/mp3')
    with col3:
        stop_button_placeholder = st.empty()
        stop_button_placeholder.button("Stop", on_click=stop_generation, key="stop_button_2", help="Click to stop response generation")

# Add buttons for saving and starting a new chat
col1, col2 = st.columns(2)
with col1:
    if st.button("Save Chat", key="save_chat_button"):
        st.session_state["show_save_input"] = True
with col2:
    if st.button("New Chat", key="new_chat_button"):
        start_new_chat()

# Input field to enter the chat name for saving, shown only when Save Chat is clicked
if st.session_state["show_save_input"]:
    chat_name = st.text_input("Enter chat name to save:", key="save_chat_input")
    if st.button("Confirm Save", key="confirm_save_button") and chat_name:
        save_chat(chat_name)

display_archived_chats()

# JavaScript to ensure Enter key triggers the input
st.markdown("""
    <script>
    const inputBox = document.getElementById('input_box');
    inputBox.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            document.getElementById('send_button').click();
        }
    });
    </script>
""", unsafe_allow_html=True)
