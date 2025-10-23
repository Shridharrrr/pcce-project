from pydantic import BaseModel
from typing import List

class Users(BaseModel):
    userId: str
    name: str
    email: str
    myTeams: List[str]
