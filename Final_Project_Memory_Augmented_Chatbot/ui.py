import streamlit as st
import requests
from gtts import gTTS
import io

# Page configuration
st.set_page_config(page_title="KnoGraph AI", page_icon="🧠")
st.title("KnoGraph AI 🧠")
st.subheader("Memory-Augmented Hybrid RAG Assistant")

# 1. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# CSS: Fix chat input at the bottom of the page
st.markdown("""
    <style>
        [data-testid="stChatInputContainer"] {
            position: fixed;
            bottom: 20px;
            width: 90%;
            margin-left: 5%;
        }
    </style>
""", unsafe_allow_html=True)

# Audio Toggle Switch
enable_audio = st.toggle("Enable Voice Response", value=False)

# 2. Display all messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
query = st.chat_input("Ask me anything...", key="my_input")

if query:
    # User message display and save
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.spinner("Thinking..."):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                "http://127.0.0.1:8000/chat", 
                json={"query": query}, 
                headers=headers,
                timeout=45
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_reply = data.get("response", "No response found.")
                
                # Assistant response display and save
                st.chat_message("assistant").write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
                # Audio response logic (RAM-based)
                if enable_audio:
                    tts = gTTS(text=bot_reply, lang='en')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3")
            else:
                st.error(f"Server error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Frontend error: {str(e)}")