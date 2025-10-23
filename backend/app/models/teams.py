from pydantic import BaseModel
from typing import List
from datetime import datetime

class Teams(BaseModel):
    teamId: str
    Admin: str
    TeamName: str
    members: List[str]
    createdAt: datetime