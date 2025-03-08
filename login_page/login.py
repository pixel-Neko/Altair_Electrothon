import streamlit as st
import firebase_config  # Import Firebase setup
from firebase_admin import auth

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None

# Function to create a new user
def signup(email, password, username):
    try:
        user = auth.create_user(email=email, password=password)
        firebase_config.users_ref.document(user.uid).set({"email": email, "username": username})
        st.success("Signup successful! You can now log in.")
    except Exception as e:
        st.error(f"Error: {e}")

# Function to verify login
def login(email, password):
    try:
        users = firebase_config.users_ref.where("email", "==", email).get()
        if users:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login Successful! 🎉")
        else:
            st.error("Invalid credentials.")
    except Exception as e:
        st.error(f"Error: {e}")

# Function to log out
def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.success("Logged out successfully!")

# UI: Show different views based on login state
if st.session_state.logged_in:
    st.subheader(f"Welcome, {st.session_state.user_email} 👋")
    if st.button("Logout"):
        logout()
else:
    st.title("🔥 Login / Signup")
    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    if menu == "Signup":
        st.subheader("Create a new account")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            signup(email, password, username)

    elif menu == "Login":
        st.subheader("Login to your account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(email, password)
