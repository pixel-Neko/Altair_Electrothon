import firebase_admin
from firebase_admin import credentials, auth, firestore

# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\aryan\Downloads\fall-d-44e4c-firebase-adminsdk-fbsvc-fbb6293f5f.json")
    firebase_admin.initialize_app(cred)

# Firestore DB instance
db = firestore.client()
users_ref = db.collection("users")
