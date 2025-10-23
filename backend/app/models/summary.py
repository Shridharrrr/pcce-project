from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SummaryCreate(BaseModel):
    team_id: str
    message_count: Optional[int] = None

class Summary(BaseModel):
    summary_id: str
    team_id: str
    content: str  # Gemini summary only
    total_messages: int
    text_messages_count: int
    participants: List[str]
    participant_count: int
    created_by: str
    creator_email: str
    created_at: datetime

class SummaryResponse(BaseModel):
    summary_id: str
    team_id: str
    content: str  # Gemini summary only
    total_messages: int
    text_messages_count: int
    participants: List[str]
    participant_count: int
    created_by: str
    creator_email: str
    created_at: datetime
