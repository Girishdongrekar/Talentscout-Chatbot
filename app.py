import streamlit as st
import re

# Initialize state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I’m TalentScout. Please tell me your full name."}
    ]
if "info" not in st.session_state:
    st.session_state.info = {"name": "", "email": "", "phone": ""}
if "stage" not in st.session_state:
    st.session_state.stage = "name"

# UI Layout
st.title("🧠 TalentScout Hiring Assistant")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User Input
user_input = st.chat_input("Type your response here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    info = st.session_state.info
    stage = st.session_state.stage

    if stage == "name":
        info["name"] = user_input
        st.session_state.stage = "email"
        bot_reply = f"Hi {info['name']}! Could you share your Gmail address?"
    elif stage == "email":
        if re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.(com|in)$", user_input):
            info["email"] = user_input
            st.session_state.stage = "phone"
            bot_reply = "Got it! Now please share your phone number."
        else:
            bot_reply = "⚠️ That doesn't look like a valid Gmail address."
    elif stage == "phone":
        if user_input.isdigit() and len(user_input) == 10:
            info["phone"] = user_input
            st.session_state.stage = "done"
            bot_reply = "✅ Thank you! We've recorded your details."
        else:
            bot_reply = "⚠️ Please enter a valid 10-digit phone number."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)
