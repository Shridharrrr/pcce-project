from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.team import Team
from app.services.firestore_service import create_document, get_collection, get_document
import uuid

router = APIRouter(prefix="/teams", tags=["teams"])

# Create a new team
@router.post("/")
def create_team(admin: str, teamName: str, members: list = []):
    team_id = str(uuid.uuid4())
    # Ensure admin is part of members
    if admin not in members:
        members.append(admin)
    
    team = Team(
        teamId=team_id,
        admin=admin,
        teamName=teamName,
        members=members,
        createdAt=datetime.utcnow()
    )
    create_document("teams", team_id, team.dict())
    for member_id in members:
        user = get_document("users", member_id)
        if user:
            user_teams = user.get("teams", [])
            if team_id not in user_teams:
                user_teams.append(team_id)
                update_document("users", member_id, {"teams": user_teams})
    
    return team

# Get all teams
@router.get("/")
def get_teams():
    teams = get_collection("teams")
    return teams

# Get a single team by ID
@router.get("/{teamId}")
def get_team(teamId: str):
    team = get_document("teams", teamId)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
