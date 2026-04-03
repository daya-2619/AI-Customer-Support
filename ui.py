import streamlit as st
import requests
import time
import os

# Page config
st.set_page_config(page_title="AI Support Bot", page_icon="🤖", layout="centered")

# Custom CSS (🔥 UI upgrade)
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
.chat-bubble-user {
    background-color: #1f77b4;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    color: white;
    text-align: right;
}
.chat-bubble-bot {
    background-color: #2d2d2d;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    color: white;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AI Customer Support")
st.caption("RAG + Local LLM (Ollama) powered chatbot")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    user_id = st.selectbox("Select User", ["101", "102"])

    st.markdown("---")
    st.subheader("📄 Upload Knowledge (PDF)")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        with open("data/uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ PDF uploaded! Restart backend to apply.")

    st.markdown("---")
    st.markdown("### 💡 Features")
    st.markdown("- RAG (FAQ + PDF)")
    st.markdown("- Local LLM (Ollama)")
    st.markdown("- Memory-enabled chat")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)

# Typing animation
def typing_effect(text):
    placeholder = st.empty()
    full_text = ""

    for char in text:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(0.01)

    return full_text

# Input box
user_input = st.chat_input("Ask about orders, refunds, delivery...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user bubble instantly
    st.markdown(f'<div class="chat-bubble-user">{user_input}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):

            try:
                response = requests.get(
                    "http://127.0.0.1:8000/chat",
                    params={"query": user_input, "user_id": user_id},
                    timeout=20
                )

                data = response.json()

                if "response" in data:
                    bot_reply = data["response"]
                else:
                    bot_reply = data.get("error", "⚠️ Unexpected server response")

            except Exception as e:
                bot_reply = "⚠️ Backend not running or connection failed"

        # Typing animation
        final_text = typing_effect(bot_reply)

    # Save bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_text
    })

    st.rerun()