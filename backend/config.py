import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    # Get the path to the service account file
    service_account_path = os.path.join(os.path.dirname(__file__), "firebase-service-account.json")
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()