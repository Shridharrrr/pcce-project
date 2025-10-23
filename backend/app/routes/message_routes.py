from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List, Optional
from app.models.message import Message, MessageCreate, MessageUpdate, MessageStatus
from app.services.firestore_service import (
    create_document, get_document, get_team_messages as fetch_team_messages, 
    update_document, delete_document, get_user_by_email
)
from app.dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=Message)
async def create_message(
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new message in a team chat"""
    # Verify user is member of the team
    team = get_document("teams", message_data.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    user_email = current_user.get("email")
    
    # Check if user is member of this team
    is_member = (team.get("admin_id") == user_id or 
                any(member.get("user_id") == user_id for member in team.get("members", [])))
    
    if not is_member:
        raise HTTPException(status_code=403, detail="You are not a member of this team")
    
    # Get or create user info for sender details
    user_info = get_user_by_email(user_email)
    if not user_info:
        # Auto-create user profile if it doesn't exist
        user_info = {
            "userId": user_id,
            "name": current_user.get("name", user_email.split("@")[0]),
            "email": user_email,
            "myTeams": [],
            "created_at": datetime.utcnow()
        }
        create_document("users", user_id, user_info)
    
    sender_name = user_info.get("name", user_email.split("@")[0])
    
    message_id = str(uuid.uuid4())
    message = Message(
        messageId=message_id,
        teamId=message_data.team_id,
        senderId=user_id,
        sender_email=user_email,
        sender_name=sender_name,
        content=message_data.content,
        message_type=message_data.message_type,
        metadata=message_data.metadata,
        status=MessageStatus.SENT,
        created_at=datetime.utcnow()
    )
    
    create_document("messages", message_id, message.dict())
    
    # Update team's last message timestamp
    update_document("teams", message_data.team_id, {"last_message_at": datetime.utcnow()})
    
    return message

@router.get("/{team_id}", response_model=List[Message])
async def get_team_messages_endpoint(
    team_id: str,
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get messages for a specific team"""
    # Verify user is member of the team
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    
    # Check if user is member of this team
    is_member = (team.get("admin_id") == user_id or 
                any(member.get("user_id") == user_id for member in team.get("members", [])))
    
    if not is_member:
        raise HTTPException(status_code=403, detail="You are not a member of this team")
    
    messages = fetch_team_messages(team_id, limit)
    return messages


@router.put("/{message_id}", response_model=Message)
async def update_message(
    message_id: str,
    message_update: MessageUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a message (only by sender)"""
    message = get_document("messages", message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    user_id = current_user.get("uid")
    if message.get("senderId") != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own messages")
    
    update_data = message_update.dict(exclude_unset=True)
    if update_data:
        update_document("messages", message_id, update_data)
        message.update(update_data)
    
    return message

@router.delete("/{message_id}")
async def delete_message(
    message_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a message (only by sender or team admin)"""
    message = get_document("messages", message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    user_id = current_user.get("uid")
    
    # Check if user is sender or team admin
    team = get_document("teams", message.get("teamId"))
    is_admin = team and team.get("admin_id") == user_id
    is_sender = message.get("senderId") == user_id
    
    if not (is_sender or is_admin):
        raise HTTPException(status_code=403, detail="You can only delete your own messages or be team admin")
    
    delete_document("messages", message_id)
    return {"message": "Message deleted successfully"}

@router.post("/{message_id}/react")
async def add_reaction(
    message_id: str,
    emoji: str,
    current_user: dict = Depends(get_current_user)
):
    """Add a reaction to a message"""
    message = get_document("messages", message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    user_email = current_user.get("email")
    reactions = message.get("reactions", {})
    
    if emoji not in reactions:
        reactions[emoji] = []
    
    # Add user to reaction if not already there
    if user_email not in reactions[emoji]:
        reactions[emoji].append(user_email)
        update_document("messages", message_id, {"reactions": reactions})
        return {"message": "Reaction added successfully"}
    
    raise HTTPException(status_code=400, detail="You have already reacted with this emoji")

@router.delete("/{message_id}/react")
async def remove_reaction(
    message_id: str,
    emoji: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove a reaction from a message"""
    message = get_document("messages", message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    user_email = current_user.get("email")
    reactions = message.get("reactions", {})
    
    if emoji in reactions and user_email in reactions[emoji]:
        reactions[emoji].remove(user_email)
        # Remove emoji if no reactions left
        if not reactions[emoji]:
            del reactions[emoji]
        update_document("messages", message_id, {"reactions": reactions})
        return {"message": "Reaction removed successfully"}
    
    raise HTTPException(status_code=400, detail="Reaction not found")

@router.post("/{message_id}/reply", response_model=Message)
async def reply_to_message(
    message_id: str,
    content: str,
    current_user: dict = Depends(get_current_user)
):
    """Reply to a specific message"""
    original_message = get_document("messages", message_id)
    if not original_message:
        raise HTTPException(status_code=404, detail="Original message not found")
    
    # Verify user is member of the team
    team = get_document("teams", original_message.get("teamId"))
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    user_email = current_user.get("email")
    
    # Check if user is member of this team
    is_member = (team.get("admin_id") == user_id or 
                any(member.get("user_id") == user_id for member in team.get("members", [])))
    
    if not is_member:
        raise HTTPException(status_code=403, detail="You are not a member of this team")
    
    # Get or create user info for sender details
    user_info = get_user_by_email(user_email)
    if not user_info:
        # Auto-create user profile if it doesn't exist
        user_info = {
            "userId": user_id,
            "name": current_user.get("name", user_email.split("@")[0]),
            "email": user_email,
            "myTeams": [],
            "created_at": datetime.utcnow()
        }
        create_document("users", user_id, user_info)
    
    sender_name = user_info.get("name", user_email.split("@")[0])
    
    reply_id = str(uuid.uuid4())
    reply = Message(
        messageId=reply_id,
        teamId=original_message.get("teamId"),
        senderId=user_id,
        sender_email=user_email,
        sender_name=sender_name,
        content=content,
        reply_to=message_id,
        status=MessageStatus.SENT,
        created_at=datetime.utcnow()
    )
    
    create_document("messages", reply_id, reply.dict())
    
    # Update team's last message timestamp
    update_document("teams", original_message.get("teamId"), {"last_message_at": datetime.utcnow()})
    
    return reply