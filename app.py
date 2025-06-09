import streamlit as st
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys from .env
load_dotenv()

# OpenRouter API config
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")  # Example: https://openrouter.ai/api/v1
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I’m TalentScout, your AI hiring assistant. I’ll collect your basic details, tech stack, and ask you a few questions to assess your fit. You can type 'exit' anytime to end the session. Let’s begin!\n\nPlease tell me your full name."}
    ]
if "info" not in st.session_state:
    st.session_state.info = {"name": "", "email": "", "phone": "", "experience": "", "position": "", "location": "", "stack": ""}
if "stage" not in st.session_state:
    st.session_state.stage = "name"

# Function to generate tech questions
def generate_tech_questions(stack):
    prompt = f"""You are a technical recruiter assistant.
A candidate has declared their tech stack as: {stack}.
Generate 3 to 5 technical questions that assess their knowledge. Also add a Note for recruiter to ask follow-up questions based on the candidate's answers."""
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=st.session_state.messages + [{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating questions: {str(e)}"

# UI layout
st.title("🧠 TalentScout Hiring Assistant")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
user_input = st.chat_input("Type your response here...")

if user_input:
    user_input = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exit check
    if user_input.lower() in ["exit", "quit", "thanks", "thank you"]:
        bot_reply = "✅ Thank you for chatting with TalentScout. Goodbye! 👋"
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").markdown(bot_reply)

        # 🔁 Reset conversation
        st.session_state.stage = "name"
        st.session_state.info = {"name": "", "email": "", "phone": "", "experience": "", "position": "", "location": "", "stack": ""}
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I’m TalentScout, your AI hiring assistant. I’ll collect your basic details, tech stack, and ask you a few questions to assess your fit. You can type 'exit' anytime to end the session. Let’s begin!\n\nPlease tell me your full name."}
        ]
        st.rerun()

    # Handle conversation flow
    stage = st.session_state.stage
    info = st.session_state.info

    if stage == "name":
        info["name"] = user_input
        st.session_state.stage = "email"
        bot_reply = f"Hi {info['name']}! Could you share your Gmail address?"

    elif stage == "email":
        gmail_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.(com|in)$"
        if re.match(gmail_pattern, user_input):
            info["email"] = user_input
            st.session_state.stage = "phone"
            bot_reply = "Got it! Now please share your phone number."
        else:
            bot_reply = "⚠️ That doesn't look like a valid Gmail address."

    elif stage == "phone":
        if user_input.isdigit() and len(user_input) == 10:
            info["phone"] = user_input
            st.session_state.stage = "experience"
            bot_reply = "Thanks! How many years of experience do you have?"
        else:
            bot_reply = "⚠️ Please enter a valid 10-digit phone number (numbers only)."

    elif stage == "experience":
        if user_input.isdigit():
            experience_years = int(user_input)
            if 0 <= experience_years <= 15:
                info["experience"] = user_input
                st.session_state.stage = "position"
                bot_reply = "Noted. What position are you applying for?"
            else:
                bot_reply = "⚠️ Please enter your experience as a number between 0 and 15."
        else:
            bot_reply = "⚠️ Please enter your experience (e.g., 3, 10)."

    elif stage == "position":
        info["position"] = user_input
        st.session_state.stage = "location"
        bot_reply = "Thanks! Where are you currently located?"

    elif stage == "location":
        info["location"] = user_input
        st.session_state.stage = "stack"
        bot_reply = "Now tell me your tech stack (languages, frameworks, databases, tools)."

    elif stage == "stack":
        info["stack"] = user_input
        st.session_state.stage = "questions"
        bot_reply = "Great! Let me generate a few technical questions for you..."
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").markdown(bot_reply)
        questions = generate_tech_questions(info["stack"])
        st.session_state.messages.append({"role": "assistant", "content": questions})
        st.chat_message("assistant").markdown(questions)
        st.session_state.stage = "done"
        st.stop()

    else:
        # Optional follow-up flow
        bot_reply = generate_tech_questions(user_input)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)
