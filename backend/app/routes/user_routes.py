from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.services.firestore_service import create_document, get_document, get_collection, update_document
import uuid

router = APIRouter(prefix="/users", tags=["users"])

# Create a new user
@router.post("/")
def create_user(name: str, email: str):
    user_id = str(uuid.uuid4())
    user = User(userId=user_id, name=name, email=email, teams=[])
    create_document("users", user_id, user.dict())
    return user

# Get a user by ID
@router.get("/{userId}")
def get_user(userId: str):
    user = get_document("users", userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get all teams/projects of a user
@router.get("/{userId}/teams")
def get_user_teams(userId: str):
    user = get_document("users", userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Fetch team details
    teams = []
    for team_id in user.get("teams", []):
        team = get_document("teams", team_id)
        if team:
            teams.append(team)
    return teams
