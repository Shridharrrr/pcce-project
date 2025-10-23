from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    messageId: str
    teamId: str
    senderId: str
    content: str
    tags: Optional[List[str]] = []  # AI detected tags like "decision" or "action_item"
    createdAt: datetime
