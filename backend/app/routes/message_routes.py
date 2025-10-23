from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.message import Message
from app.services.firestore_service import create_document, get_collection
import uuid

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/")
def create_message(teamId: str, senderId: str, content: str):
    message_id = str(uuid.uuid4())
    message = Message(
        messageId=message_id,
        teamId=teamId,
        senderId=senderId,
        content=content,
        createdAt=datetime.utcnow()
    )
    create_document("messages", message_id, message.dict())
    return message

@router.get("/{teamId}")
def get_messages(teamId: str):
    messages = get_collection("messages")
    team_messages = [m for m in messages if m["teamId"] == teamId]
    return team_messages
