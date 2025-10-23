import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    if os.path.exists("firebase-service-account.json"):
        try:
            cred = credentials.Certificate("firebase-service-account.json")
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully")
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            print("Please configure Firebase properly to use authentication features")
            # Initialize with default app for development
            firebase_admin.initialize_app()
    else:
        print("Firebase service account file not found. Please add firebase-service-account.json")
        print("Initializing Firebase without credentials for development")
        firebase_admin.initialize_app()

# Firestore client
try:
    db = firestore.client()
    print("Firestore client initialized")
except Exception as e:
    print(f"Firestore client initialization failed: {e}")
    print("Firestore operations will not work without proper Firebase configuration")
    db = None