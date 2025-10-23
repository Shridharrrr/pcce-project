from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"

class MessageStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

class MessageBase(BaseModel):
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Optional[Dict[str, Any]] = None

class MessageCreate(MessageBase):
    team_id: str
    sender_email: EmailStr

class MessageUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class Message(MessageBase):
    messageId: str
    teamId: str
    senderId: str
    sender_email: str
    sender_name: str
    tags: Optional[List[str]] = []  # AI detected tags like "decision" or "action_item"
    status: MessageStatus = MessageStatus.SENT
    created_at: datetime
    updated_at: Optional[datetime] = None
    reply_to: Optional[str] = None  # ID of message this is replying to
    reactions: Optional[Dict[str, List[str]]] = {}  # emoji -> list of user emails who reacted

class ChatRoom(BaseModel):
    room_id: str
    team_id: str
    name: str
    description: Optional[str] = None
    created_by: str
    created_at: datetime
    is_active: bool = True
    last_message_at: Optional[datetime] = None
