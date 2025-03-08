import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\aryan\Downloads\fall-d-44e4c-firebase-adminsdk-fbsvc-fbb6293f5f.json")  # Use your Firebase JSON key
firebase_admin.initialize_app(cred)

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        return str(e)

def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception as e:
        return str(e)
