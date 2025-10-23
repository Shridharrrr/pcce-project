from app.config import db

def create_document(collection_name: str, doc_id: str, data: dict):
    db.collection(collection_name).document(doc_id).set(data)
    return data

def get_document(collection_name: str, doc_id: str):
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_collection(collection_name: str):
    docs = db.collection(collection_name).stream()
    return [doc.to_dict() for doc in docs]

def update_document(collection_name: str, doc_id: str, data: dict):
    db.collection(collection_name).document(doc_id).update(data)
