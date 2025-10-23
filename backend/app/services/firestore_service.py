from app.config import db
from typing import List, Dict, Any, Optional
from datetime import datetime

def create_document(collection_name: str, doc_id: str, data: dict):
    """Create a new document in Firestore"""
    if db is None:
        raise Exception("Firestore not configured")
    db.collection(collection_name).document(doc_id).set(data)
    return data

def get_document(collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
    """Get a single document from Firestore"""
    if db is None:
        raise Exception("Firestore not configured")
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_collection(collection_name: str) -> List[Dict[str, Any]]:
    """Get all documents from a collection"""
    if db is None:
        raise Exception("Firestore not configured")
    docs = db.collection(collection_name).stream()
    return [doc.to_dict() for doc in docs]

def update_document(collection_name: str, doc_id: str, data: dict):
    """Update a document in Firestore"""
    if db is None:
        raise Exception("Firestore not configured")
    data["updated_at"] = datetime.utcnow()
    db.collection(collection_name).document(doc_id).update(data)
    return data

def delete_document(collection_name: str, doc_id: str):
    """Delete a document from Firestore"""
    if db is None:
        raise Exception("Firestore not configured")
    db.collection(collection_name).document(doc_id).delete()
    return True

def query_collection(collection_name: str, field: str, operator: str, value: Any) -> List[Dict[str, Any]]:
    """Query a collection with a specific condition"""
    if db is None:
        raise Exception("Firestore not configured")
    docs = db.collection(collection_name).where(field, operator, value).stream()
    return [doc.to_dict() for doc in docs]

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email address"""
    users = query_collection("users", "email", "==", email)
    return users[0] if users else None

def get_team_messages(team_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get messages for a specific team, ordered by creation time"""
    if db is None:
        raise Exception("Firestore not configured")
    messages_ref = db.collection("messages").where("teamId", "==", team_id)
    messages_ref = messages_ref.order_by("created_at", direction="DESCENDING").limit(limit)
    docs = messages_ref.stream()
    return [doc.to_dict() for doc in docs]

def get_user_teams(user_id: str) -> List[Dict[str, Any]]:
    """Get all teams a user is a member of"""
    if db is None:
        raise Exception("Firestore not configured")
    teams_ref = db.collection("teams")
    docs = teams_ref.stream()
    user_teams = []
    for doc in docs:
        team_data = doc.to_dict()
        # Check if user is admin or member
        if (team_data.get("admin_id") == user_id or 
            any(member.get("user_id") == user_id for member in team_data.get("members", []))):
            user_teams.append(team_data)
    return user_teams

def add_team_member(team_id: str, member_data: Dict[str, Any]):
    """Add a member to a team"""
    if db is None:
        raise Exception("Firestore not configured")
    team_ref = db.collection("teams").document(team_id)
    team_doc = team_ref.get()
    
    if team_doc.exists:
        team_data = team_doc.to_dict()
        members = team_data.get("members", [])
        
        # Check if member already exists
        if not any(member.get("user_id") == member_data["user_id"] for member in members):
            members.append(member_data)
            team_ref.update({"members": members, "updated_at": datetime.utcnow()})
            return True
    return False

def remove_team_member(team_id: str, user_id: str):
    """Remove a member from a team"""
    if db is None:
        raise Exception("Firestore not configured")
    team_ref = db.collection("teams").document(team_id)
    team_doc = team_ref.get()
    
    if team_doc.exists:
        team_data = team_doc.to_dict()
        members = team_data.get("members", [])
        
        # Remove member
        members = [member for member in members if member.get("user_id") != user_id]
        team_ref.update({"members": members, "updated_at": datetime.utcnow()})
        return True
    return False
