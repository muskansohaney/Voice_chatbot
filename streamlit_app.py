# streamlit_app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # if using an API; otherwise run assistant in same process

st.set_page_config(page_title="Custom AI Assistant", layout="wide")
st.title("Custom AI Assistant — voice & text")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Input area
with st.form("input_form"):
    user_text = st.text_area("Say something (or use voice file upload):", height=120)
    #audio_file = st.file_uploader("Or upload audio (wav) for speech→text (optional)", type=["wav", "mp3"], accept_multiple_files=False)
    submit = st.form_submit_button("Send")

if submit:
    # If audio provided, you could send audio to backend for STT.
    payload = {"text": user_text}
    # simple direct call to run locally (if same process), or call your HTTP backend
    # We'll call a local endpoint for demo:
    try:
        resp = requests.post(f"{BACKEND_URL}/api/message", json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        assistant_text = data.get("assistant")
    except Exception as e:
        assistant_text = f"[Error contacting backend: {e}]"

    # Append to chat state
    st.session_state.messages.append({"role": "user", "text": user_text})
    st.session_state.messages.append({"role": "assistant", "text": assistant_text})

# Show messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Assistant:** {msg['text']}")


import streamlit as st
import requests

st.title("🎤 Voice + Text Chatbot (Groq + Redis)")

backend_url = "http://localhost:8000/api"

uploaded_file = st.file_uploader("Upload a voice message", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    with st.spinner("Processing voice..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{backend_url}/voice", files=files)
        data = response.json()
        st.write("🗣️ You said:", data["input_text"])
        st.write("🤖 Bot replied:", data["reply"])

#cd Text_chatbot
#source .venv/bin/activate
#streamlit run streamlit_app.py
