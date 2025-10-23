from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List
from app.models.todo import Todo, TodoCreate, TodoResponse, AssignedUser
from app.services.firestore_service import (
    create_todo, get_todo, get_team_todos, get_user_todos,
    delete_todo, get_user_by_email, get_document
)
from app.dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    todo_data: TodoCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new todo"""
    todo_id = str(uuid.uuid4())
    creator_email = current_user.get("email")
    creator_id = current_user.get("uid")
    
    # Get creator info
    creator_user = get_user_by_email(creator_email)
    if not creator_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator user not found"
        )
    
    # Verify team exists
    team = get_document("teams", todo_data.team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    # Build assigned users list
    assigned_users = []
    for email in todo_data.assigned_user_emails:
        user = get_user_by_email(email)
        if user:
            assigned_users.append({
                "user_id": user["userId"],
                "email": email,
                "name": user.get("name", email.split("@")[0]),
                "assigned_at": datetime.utcnow().isoformat()
            })
    
    # Create todo document
    now = datetime.utcnow()
    todo_doc = {
        "todo_id": todo_id,
        "team_id": todo_data.team_id,
        "title": todo_data.title,
        "description": todo_data.description,
        "deadline": todo_data.deadline.isoformat() if todo_data.deadline else None,
        "priority": todo_data.priority.value if hasattr(todo_data.priority, 'value') else todo_data.priority,
        "status": todo_data.status.value if hasattr(todo_data.status, 'value') else todo_data.status,
        "created_by": creator_id,
        "creator_email": creator_email,
        "creator_name": creator_user.get("name", creator_email.split("@")[0]),
        "assigned_users": assigned_users,
        "created_at": now.isoformat(),
        "updated_at": None,
        "completed_at": None
    }
    
    create_todo(todo_id, todo_doc)
    
    # Convert back to response model with proper datetime objects
    assigned_users_response = [
        AssignedUser(
            user_id=user["user_id"],
            email=user["email"],
            name=user["name"],
            assigned_at=datetime.fromisoformat(user["assigned_at"])
        )
        for user in assigned_users
    ]
    
    return TodoResponse(
        todo_id=todo_id,
        team_id=todo_data.team_id,
        title=todo_data.title,
        description=todo_data.description,
        deadline=todo_data.deadline,
        priority=todo_data.priority,
        status=todo_data.status,
        created_by=creator_id,
        creator_email=creator_email,
        creator_name=creator_user.get("name", creator_email.split("@")[0]),
        assigned_users=assigned_users_response,
        created_at=now,
        updated_at=None,
        completed_at=None
    )

@router.get("/team/{team_id}", response_model=List[TodoResponse])
async def get_todos_by_team(
    team_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all todos for a specific team"""
    # Verify team exists and user has access
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    user_id = current_user.get("uid")
    # Check if user is admin or member
    is_member = (
        team.get("admin_id") == user_id or
        any(member.get("user_id") == user_id for member in team.get("members", []))
    )
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this team"
        )
    
    todos = get_team_todos(team_id)
    
    # Convert to response models
    result = []
    for todo in todos:
        assigned_users = [
            AssignedUser(
                user_id=user["user_id"],
                email=user["email"],
                name=user["name"],
                assigned_at=datetime.fromisoformat(user["assigned_at"])
            )
            for user in todo.get("assigned_users", [])
        ]
        
        result.append(TodoResponse(
            todo_id=todo["todo_id"],
            team_id=todo["team_id"],
            title=todo["title"],
            description=todo.get("description"),
            deadline=datetime.fromisoformat(todo["deadline"]) if todo.get("deadline") else None,
            priority=todo["priority"],
            status=todo["status"],
            created_by=todo["created_by"],
            creator_email=todo["creator_email"],
            creator_name=todo["creator_name"],
            assigned_users=assigned_users,
            created_at=datetime.fromisoformat(todo["created_at"]),
            updated_at=datetime.fromisoformat(todo["updated_at"]) if todo.get("updated_at") else None,
            completed_at=datetime.fromisoformat(todo["completed_at"]) if todo.get("completed_at") else None
        ))
    
    return result

@router.get("/my-todos", response_model=List[TodoResponse])
async def get_my_todos(
    current_user: dict = Depends(get_current_user)
):
    """Get all todos assigned to the current user"""
    user_email = current_user.get("email")
    todos = get_user_todos(user_email)
    
    # Convert to response models
    result = []
    for todo in todos:
        assigned_users = [
            AssignedUser(
                user_id=user["user_id"],
                email=user["email"],
                name=user["name"],
                assigned_at=datetime.fromisoformat(user["assigned_at"])
            )
            for user in todo.get("assigned_users", [])
        ]
        
        result.append(TodoResponse(
            todo_id=todo["todo_id"],
            team_id=todo["team_id"],
            title=todo["title"],
            description=todo.get("description"),
            deadline=datetime.fromisoformat(todo["deadline"]) if todo.get("deadline") else None,
            priority=todo["priority"],
            status=todo["status"],
            created_by=todo["created_by"],
            creator_email=todo["creator_email"],
            creator_name=todo["creator_name"],
            assigned_users=assigned_users,
            created_at=datetime.fromisoformat(todo["created_at"]),
            updated_at=datetime.fromisoformat(todo["updated_at"]) if todo.get("updated_at") else None,
            completed_at=datetime.fromisoformat(todo["completed_at"]) if todo.get("completed_at") else None
        ))
    
    return result

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo_by_id(
    todo_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific todo by ID"""
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Verify user has access to the team
    team = get_document("teams", todo["team_id"])
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    user_id = current_user.get("uid")
    is_member = (
        team.get("admin_id") == user_id or
        any(member.get("user_id") == user_id for member in team.get("members", []))
    )
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this todo"
        )
    
    assigned_users = [
        AssignedUser(
            user_id=user["user_id"],
            email=user["email"],
            name=user["name"],
            assigned_at=datetime.fromisoformat(user["assigned_at"])
        )
        for user in todo.get("assigned_users", [])
    ]
    
    return TodoResponse(
        todo_id=todo["todo_id"],
        team_id=todo["team_id"],
        title=todo["title"],
        description=todo.get("description"),
        deadline=datetime.fromisoformat(todo["deadline"]) if todo.get("deadline") else None,
        priority=todo["priority"],
        status=todo["status"],
        created_by=todo["created_by"],
        creator_email=todo["creator_email"],
        creator_name=todo["creator_name"],
        assigned_users=assigned_users,
        created_at=datetime.fromisoformat(todo["created_at"]),
        updated_at=datetime.fromisoformat(todo["updated_at"]) if todo.get("updated_at") else None,
        completed_at=datetime.fromisoformat(todo["completed_at"]) if todo.get("completed_at") else None
    )

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(
    todo_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a todo"""
    todo = get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Verify user is creator or team admin
    team = get_document("teams", todo["team_id"])
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    user_id = current_user.get("uid")
    is_creator = todo["created_by"] == user_id
    is_admin = team.get("admin_id") == user_id
    
    if not (is_creator or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator or team admin can delete this todo"
        )
    
    delete_todo(todo_id)
    return None
