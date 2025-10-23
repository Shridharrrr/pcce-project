from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    userId: str
    myTeams: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True

class UserProfile(BaseModel):
    userId: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
