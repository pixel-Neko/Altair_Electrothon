import streamlit as st
import google.generativeai as genai
from firebase_config import register_user, login_user

# Set up Gemini API
genai.configure(api_key="AIzaSyDuNCt9U-RBn4pNOXS_focEyMH1hmT8q2c")  # Replace with your key

st.title("🔥 Streamlit Login + Gemini AI Chatbot")

# Session management
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login / Signup
auth_mode = st.sidebar.radio("Select Mode", ["Login", "Signup"])

if not st.session_state.authenticated:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if auth_mode == "Signup":
        if st.button("Sign Up"):
            user_id = register_user(email, password)
            st.success(f"User Created: {user_id}")
    else:
        if st.button("Login"):
            user_id = login_user(email, password)
            if "auth" not in user_id:
                st.session_state.authenticated = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# If logged in, show chatbot
if st.session_state.authenticated:
    st.subheader("Chat with Gemini AI 🤖")
    
    user_input = st.text_area("Type your message...")
    if st.button("Ask Gemini"):
        model = genai.GenerativeModel("gemini-2.0-pro-exp")
        response = model.generate_content(user_input)
        st.write("### 🤖 Gemini AI Response:")
        st.write(response.text)
