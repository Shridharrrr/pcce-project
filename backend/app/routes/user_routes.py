from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List, Optional
from app.models.users import User, UserCreate, UserUpdate, UserProfile
from app.services.firestore_service import (
    create_document, get_document, get_collection, update_document,
    get_user_by_email, get_user_teams
)
from app.dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/users", tags=["users"])

async def _create_user_internal(user_data: UserCreate):
    """Internal function to create a user (to avoid circular imports)"""
    # Check if user already exists
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_id = str(uuid.uuid4())
    user = User(
        userId=user_id,
        name=user_data.name,
        email=user_data.email,
        myTeams=[],
        created_at=datetime.utcnow()
    )
    
    create_document("users", user_id, user.dict())
    return user

@router.post("/", response_model=User)
async def create_user(user_data: UserCreate):
    """Create a new user"""
    return await _create_user_internal(user_data)

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user's profile"""
    user_id = current_user.get("uid")
    user_email = current_user.get("email")
    
    # Try to get user from our database first
    user = get_document("users", user_id)
    if not user:
        # If not found, try to get by email
        user = get_user_by_email(user_email)
        if not user:
            # Create user profile from Firebase auth data
            user_data = UserCreate(
                name=current_user.get("name", user_email.split("@")[0]),
                email=user_email
            )
            user = await _create_user_internal(user_data)
    
    return UserProfile(
        userId=user["userId"],
        name=user["name"],
        email=user["email"],
        avatar_url=current_user.get("picture"),
        created_at=user.get("created_at", datetime.utcnow())
    )

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get a user by ID"""
    user = get_document("users", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user's profile"""
    user_id = current_user.get("uid")
    user = get_document("users", user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_document("users", user_id, update_data)
        user.update(update_data)
    
    return user

@router.get("/me/teams")
async def get_current_user_teams(current_user: dict = Depends(get_current_user)):
    """Get all teams for the current user"""
    user_id = current_user.get("uid")
    teams = get_user_teams(user_id)
    return teams

@router.get("/{user_id}/teams")
async def get_specific_user_teams(user_id: str, current_user: dict = Depends(get_current_user)):
    """Get all teams for a specific user"""
    user = get_document("users", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    teams = get_user_teams(user_id)
    return teams

@router.get("/search/{email}")
async def search_user_by_email(email: str, current_user: dict = Depends(get_current_user)):
    """Search for a user by email address"""
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return basic user info (no sensitive data)
    return {
        "userId": user["userId"],
        "name": user["name"],
        "email": user["email"]
    }
