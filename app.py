import streamlit as st

# Initialize chatbot messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I’m TalentScout, your AI hiring assistant. Please tell me your full name."}
    ]

# UI Layout
st.title("🧠 TalentScout Hiring Assistant")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
user_input = st.chat_input("Type your response here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = "Thanks! We'll process your input soon."
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)
