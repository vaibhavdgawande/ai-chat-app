import streamlit as st
import requests

st.title("My Local AI Chat")
st.write("Type a message below and your local AI will reply.")

# This keeps messages remembered even as the page reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"You: {msg['content']}")
    else:
        st.write(f"AI: {msg['content']}")

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": user_input, "stream": False}
        )
        ai_reply = response.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.rerun()