import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()