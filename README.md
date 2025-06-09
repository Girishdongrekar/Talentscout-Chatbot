# 🧠 TalentScout - AI Hiring Assistant

A Streamlit-based AI chatbot that helps recruiters assess candidates' fit by collecting basic info and generating tech-stack-based questions using OpenRouter LLM.

## Setup
1. Clone the repo
2. Add `.env` with API keys
3. Install requirements
4. Run: `streamlit run main.py`
# Talentscout-Chatbot
The TalentScout AI Hiring Assistant is a conversational chatbot developed using Streamlit and OpenAI-compatible models via OpenRouter. It collects essential candidate information such as name, email, phone number, experience, location, position, and tech stack in a structured flow. Once the user inputs their tech stack, the assistant uses an LLM (e.g., DeepSeek) to generate 3–5 relevant technical questions along with a note for human recruiters to ask follow-up queries. All data validation is handled on the frontend using regex and logical checks to ensure data integrity.

The code structure is modular and uses st.session_state to manage conversation stages and store user responses. The chatbot's flow is state-driven, making it easy to extend or modify any individual stage (e.g., adding resume upload or branching questions). Sensitive API keys and endpoints are loaded via a .env file using python-dotenv, keeping the application secure and environment-agnostic. The chatbot UI and logic reside in a single app.py file for simplicity, but components can easily be split into separate modules for scalability.

To contribute, developers should clone the repository, set up their .env with valid OPENAI_API_KEY and OPENAI_BASE_URL, and install dependencies using pip install -r requirements.txt. The application can be run locally using streamlit run app.py. Key contribution areas include improving input validation, expanding the conversation flow, integrating a backend database for storing sessions, or enabling cloud deployment. The codebase is clean, self-contained, and ideal for collaborative development.
