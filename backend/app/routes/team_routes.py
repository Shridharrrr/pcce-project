from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from typing import List
from app.models.teams import Team, TeamCreate, TeamUpdate, TeamMember, TeamInvite
from app.services.firestore_service import (
    create_document, get_document, get_collection, update_document, 
    delete_document, get_user_by_email, add_team_member, remove_team_member
)
from app.dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/teams", tags=["teams"])

# Helper: Ensure Firestore user exists
def ensure_user_in_firestore(user: dict):
    """Create a Firestore user document if it does not exist."""
    user_doc = get_user_by_email(user["email"])
    if not user_doc:
        create_document("users", user["uid"], {
            "userId": user["uid"],
            "email": user["email"],
            "name": user.get("name", user["email"].split("@")[0]),
            "myTeams": []
        })
        user_doc = get_user_by_email(user["email"])
    return user_doc

# -----------------------
# Team CRUD Routes
# -----------------------

@router.post("/", response_model=Team)
async def create_team(
    team_data: TeamCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new team"""
    team_id = str(uuid.uuid4())
    admin_email = current_user.get("email")
    admin_id = current_user.get("uid")
<<<<<<< HEAD
    
    # Get or create admin user info
    admin_user = get_user_by_email(admin_email)
    if not admin_user:
        # Auto-create user profile if it doesn't exist
        admin_user = {
            "userId": admin_id,
            "name": current_user.get("name", admin_email.split("@")[0]),
            "email": admin_email,
            "myTeams": [],
            "created_at": datetime.utcnow()
        }
        create_document("users", admin_id, admin_user)
    
=======

    # Ensure admin user exists in Firestore
    admin_user = ensure_user_in_firestore(current_user)

>>>>>>> 065ca67c67fd18d8d229eaf68ed59a384117ba53
    # Create team members list starting with admin
    members = [TeamMember(
        user_id=admin_id,
        email=admin_email,
        name=admin_user.get("name", admin_email.split("@")[0]),
        role="admin",
        joined_at=datetime.utcnow()
    )]

    # Add other members if provided
    for member_email in team_data.member_emails:
        if member_email != admin_email:
            member_user = get_user_by_email(member_email)
            if member_user:
                members.append(TeamMember(
                    user_id=member_user["userId"],
                    email=member_email,
                    name=member_user.get("name", member_email.split("@")[0]),
                    role="member",
                    joined_at=datetime.utcnow()
                ))
            else:
                # Create invitation for non-existing users
                invite_id = str(uuid.uuid4())
                invite = TeamInvite(
                    team_id=team_id,
                    inviter_email=admin_email,
                    invitee_email=member_email,
                    role="member",
                    status="pending",
                    created_at=datetime.utcnow(),
                    expires_at=datetime.utcnow() + timedelta(days=7)
                )
                create_document("team_invites", invite_id, invite.dict())

    # Create the team
    team = Team(
        teamId=team_id,
        admin_id=admin_id,
        admin_email=admin_email,
        teamName=team_data.teamName,
        description=team_data.description,
        members=members,
        created_at=datetime.utcnow()
    )
    create_document("teams", team_id, team.dict())

    # Update admin user's team list
    admin_teams = admin_user.get("myTeams", [])
    if team_id not in admin_teams:
        admin_teams.append(team_id)
        update_document("users", admin_id, {"myTeams": admin_teams})

    return team

@router.get("/", response_model=List[Team])
async def get_user_teams(current_user: dict = Depends(get_current_user)):
    """Get all teams for the current user"""
    user_id = current_user.get("uid")
    teams = get_collection("teams") or []
    user_teams = [
        team for team in teams
        if team.get("admin_id") == user_id or
           any(member.get("user_id") == user_id for member in team.get("members", []))
    ]
    return user_teams

@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific team by ID"""
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    if team.get("admin_id") != user_id and \
       not any(member.get("user_id") == user_id for member in team.get("members", [])):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return team

@router.put("/{team_id}", response_model=Team)
async def update_team(
    team_id: str,
    team_update: TeamUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update team information (admin only)"""
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    if team.get("admin_id") != user_id:
        raise HTTPException(status_code=403, detail="Only team admin can update team")
    
    update_data = team_update.dict(exclude_unset=True)
    if update_data:
        update_document("teams", team_id, update_data)
        team.update(update_data)
    
    return team

# -----------------------
# Team Members
# -----------------------

@router.post("/{team_id}/members")
async def add_member_to_team(
    team_id: str,
    member_email: str,
    current_user: dict = Depends(get_current_user)
):
    """Add a member to the team by email"""
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    if team.get("admin_id") != user_id:
        raise HTTPException(status_code=403, detail="Only team admin can add members")
    
    if any(member.get("email") == member_email for member in team.get("members", [])):
        raise HTTPException(status_code=400, detail="Member already exists")
    
    member_user = get_user_by_email(member_email)
    if not member_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    member_data = {
        "user_id": member_user["userId"],
        "email": member_email,
        "name": member_user.get("name", member_email.split("@")[0]),
        "role": "member",
        "joined_at": datetime.utcnow()
    }
    
    success = add_team_member(team_id, member_data)
    if success:
        member_teams = member_user.get("myTeams", [])
        if team_id not in member_teams:
            member_teams.append(team_id)
            update_document("users", member_user["userId"], {"myTeams": member_teams})
        return {"message": "Member added successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to add member")

@router.delete("/{team_id}/members/{member_id}")
async def remove_member_from_team(
    team_id: str,
    member_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove a member from the team"""
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    if team.get("admin_id") != user_id:
        raise HTTPException(status_code=403, detail="Only team admin can remove members")
    
    if member_id == user_id:
        raise HTTPException(status_code=400, detail="Admin cannot remove themselves")
    
    success = remove_team_member(team_id, member_id)
    if success:
        member_user = get_document("users", member_id)
        if member_user:
            member_teams = member_user.get("myTeams", [])
            if team_id in member_teams:
                member_teams.remove(team_id)
                update_document("users", member_id, {"myTeams": member_teams})
        return {"message": "Member removed successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to remove member")

# -----------------------
# Team Invitations
# -----------------------

@router.post("/{team_id}/invite")
async def invite_user_to_team(
    team_id: str,
    invitee_email: str,
    current_user: dict = Depends(get_current_user)
):
    """Invite a user to join the team"""
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    if team.get("admin_id") != user_id:
        raise HTTPException(status_code=403, detail="Only team admin can send invitations")
    
    if any(member.get("email") == invitee_email for member in team.get("members", [])):
        raise HTTPException(status_code=400, detail="User is already a member")
    
    invite_id = str(uuid.uuid4())
    invite = TeamInvite(
        team_id=team_id,
        inviter_email=current_user.get("email"),
        invitee_email=invitee_email,
        role="member",
        status="pending",
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    
    create_document("team_invites", invite_id, invite.dict())
    return {"message": "Invitation sent successfully", "invite_id": invite_id}

# -----------------------
# Delete Team
# -----------------------

@router.delete("/{team_id}")
async def delete_team(team_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a team (admin only)"""
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user_id = current_user.get("uid")
    if team.get("admin_id") != user_id:
        raise HTTPException(status_code=403, detail="Only team admin can delete team")
    
    # Remove team from all members' myTeams
    for member in team.get("members", []):
        member_user = get_document("users", member["user_id"])
        if member_user:
            member_teams = member_user.get("myTeams", [])
            if team_id in member_teams:
                member_teams.remove(team_id)
                update_document("users", member["user_id"], {"myTeams": member_teams})
    
    delete_document("teams", team_id)
    return {"message": "Team deleted successfully"}
