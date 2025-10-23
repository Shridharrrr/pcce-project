from pydantic import BaseModel
from typing import List
from datetime import datetime

class Summary(BaseModel):
    summaryId: str
    teamId: str
    content: str
    relatedMessages: List[str]
    createdAt: datetime
