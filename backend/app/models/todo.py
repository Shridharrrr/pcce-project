from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class AssignedUser(BaseModel):
    user_id: str
    email: str
    name: str
    assigned_at: datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: TodoPriority = TodoPriority.MEDIUM
    status: TodoStatus = TodoStatus.PENDING

class TodoCreate(TodoBase):
    team_id: str
    assigned_user_emails: List[EmailStr] = []

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[TodoPriority] = None
    status: Optional[TodoStatus] = None
    assigned_user_emails: Optional[List[EmailStr]] = None

class Todo(TodoBase):
    todo_id: str
    team_id: str
    created_by: str
    creator_email: str
    creator_name: str
    assigned_users: List[AssignedUser] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class TodoResponse(BaseModel):
    todo_id: str
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: TodoPriority
    status: TodoStatus
    team_id: str
    created_by: str
    creator_email: str
    creator_name: str
    assigned_users: List[AssignedUser]
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
