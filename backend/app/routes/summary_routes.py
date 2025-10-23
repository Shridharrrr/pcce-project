from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import List
from app.models.summary import Summary, SummaryCreate, SummaryResponse
from app.services.firestore_service import (
    create_document, get_document, query_collection, get_team_messages
)
from app.services.gemini_service import generate_summary_from_messages
from app.dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/summaries", tags=["summaries"])

@router.post("/generate", response_model=SummaryResponse, status_code=status.HTTP_201_CREATED)
async def generate_team_summary(
    summary_data: SummaryCreate,
    current_user: dict = Depends(get_current_user)
):
    """Generate a summary for a team's chat messages using Hugging Face"""
    team_id = summary_data.team_id
    
    # Verify team exists and user has access
    team = get_document("teams", team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    user_id = current_user.get("uid")
    user_email = current_user.get("email")
    
    # Check if user is member of this team
    is_member = (
        team.get("admin_id") == user_id or
        any(member.get("user_id") == user_id for member in team.get("members", []))
    )
    
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this team"
        )
    
    # Fetch team messages
    messages = get_team_messages(team_id, limit=summary_data.message_count or 100)
    
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No messages found for this team"
        )
    
    try:
        # Generate summary directly using Gemini
        result = generate_summary_from_messages(messages)
        
        # Create summary document
        summary_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        summary_doc = {
            "summary_id": summary_id,
            "team_id": team_id,
            "content": result["summary"],
            "total_messages": result["total_messages"],
            "text_messages_count": result["text_messages_count"],
            "participants": result["participants"],
            "participant_count": result["participant_count"],
            "created_by": user_id,
            "creator_email": user_email,
            "created_at": now.isoformat()
        }
        
        # Save to Firestore
        create_document("summaries", summary_id, summary_doc)
        
        return SummaryResponse(
            summary_id=summary_id,
            team_id=team_id,
            content=result["summary"],
            total_messages=result["total_messages"],
            text_messages_count=result["text_messages_count"],
            participants=result["participants"],
            participant_count=result["participant_count"],
            created_by=user_id,
            creator_email=user_email,
            created_at=now
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}"
        )

@router.get("/team/{team_id}", response_model=List[SummaryResponse])
async def get_team_summaries(
    team_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all summaries for a specific team"""
    # Verify team exists and user has access
    team = get_document("teams", team_id)
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
            detail="You don't have access to this team"
        )
    
    # Fetch summaries for this team
    summaries = query_collection("summaries", "team_id", "==", team_id)
    
    # Convert to response models
    result = []
    for summary in summaries:
        result.append(SummaryResponse(
            summary_id=summary["summary_id"],
            team_id=summary["team_id"],
            content=summary["content"],
            total_messages=summary["total_messages"],
            text_messages_count=summary["text_messages_count"],
            participants=summary["participants"],
            participant_count=summary["participant_count"],
            created_by=summary["created_by"],
            creator_email=summary["creator_email"],
            created_at=datetime.fromisoformat(summary["created_at"])
        ))
    
    # Sort by creation date (newest first)
    result.sort(key=lambda x: x.created_at, reverse=True)
    
    return result

@router.get("/{summary_id}", response_model=SummaryResponse)
async def get_summary_by_id(
    summary_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific summary by ID"""
    summary = get_document("summaries", summary_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    # Verify user has access to the team
    team = get_document("teams", summary["team_id"])
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
            detail="You don't have access to this summary"
        )
    
    return SummaryResponse(
        summary_id=summary["summary_id"],
        team_id=summary["team_id"],
        content=summary["content"],
        total_messages=summary["total_messages"],
        text_messages_count=summary["text_messages_count"],
        participants=summary["participants"],
        participant_count=summary["participant_count"],
        created_by=summary["created_by"],
        creator_email=summary["creator_email"],
        created_at=datetime.fromisoformat(summary["created_at"])
    )

@router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_summary(
    summary_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a summary"""
    summary = get_document("summaries", summary_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Summary not found"
        )
    
    user_id = current_user.get("uid")
    
    # Only creator or team admin can delete
    team = get_document("teams", summary["team_id"])
    is_creator = summary["created_by"] == user_id
    is_admin = team and team.get("admin_id") == user_id
    
    if not (is_creator or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator or team admin can delete this summary"
        )
    
    from app.services.firestore_service import delete_document
    delete_document("summaries", summary_id)
    return None
