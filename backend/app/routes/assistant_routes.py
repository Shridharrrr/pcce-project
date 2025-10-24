from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.dependencies.auth import get_current_user
from app.services.assistant_service import assistant_service

router = APIRouter(prefix="/api/assistant", tags=["assistant"])

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    project_context: Optional[str] = None
    use_rag: bool = True

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    timestamp: str
    project_context: str

class ProjectKnowledgeRequest(BaseModel):
    project_id: str
    project_name: str
    description: str
    additional_info: Optional[Dict[str, Any]] = None

class CodeKnowledgeRequest(BaseModel):
    code_id: str
    code: str
    language: str
    description: str
    project_id: Optional[str] = None

class StatusResponse(BaseModel):
    success: bool
    message: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat with the AI assistant
    
    - **message**: User's message to the assistant
    - **project_context**: Optional project context identifier
    - **use_rag**: Whether to use RAG (Retrieval Augmented Generation)
    """
    try:
        user_id = current_user.get("uid")
        
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )
        
        # Generate response
        result = await assistant_service.generate_response(
            user_id=user_id,
            message=request.message,
            project_context=request.project_context,
            use_rag=request.use_rag
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )

@router.post("/clear-history", response_model=StatusResponse)
async def clear_conversation_history(
    project_context: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Clear conversation history for the current user (optionally for specific project)"""
    try:
        user_id = current_user.get("uid")
        assistant_service.clear_history(user_id, project_context)
        
        return StatusResponse(
            success=True,
            message=f"Conversation history cleared successfully{' for project' if project_context else ''}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear history: {str(e)}"
        )

@router.get("/history")
async def get_conversation_history(
    project_context: str = "general",
    current_user: dict = Depends(get_current_user)
):
    """Get conversation history for the current user and project"""
    try:
        user_id = current_user.get("uid")
        history = assistant_service.get_conversation_history(user_id, project_context)
        
        return {
            "history": history,
            "count": len(history),
            "project_context": project_context
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve history: {str(e)}"
        )

@router.post("/knowledge/project", response_model=StatusResponse)
async def add_project_knowledge(
    request: ProjectKnowledgeRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Add project knowledge to the assistant's knowledge base
    
    This allows the assistant to provide context-aware responses about specific projects
    """
    try:
        success = assistant_service.add_project_knowledge(
            project_id=request.project_id,
            project_name=request.project_name,
            description=request.description,
            additional_info=request.additional_info
        )
        
        if success:
            return StatusResponse(
                success=True,
                message="Project knowledge added successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add project knowledge"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add project knowledge: {str(e)}"
        )

@router.post("/knowledge/code", response_model=StatusResponse)
async def add_code_knowledge(
    request: CodeKnowledgeRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Add code snippet to the assistant's knowledge base
    
    This allows the assistant to reference and suggest code from your projects
    """
    try:
        success = assistant_service.add_code_knowledge(
            code_id=request.code_id,
            code=request.code,
            language=request.language,
            description=request.description,
            project_id=request.project_id
        )
        
        if success:
            return StatusResponse(
                success=True,
                message="Code knowledge added successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add code knowledge"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add code knowledge: {str(e)}"
        )

@router.get("/health")
async def assistant_health_check():
    """Check if the assistant service is operational"""
    try:
        return {
            "status": "healthy",
            "service": "ThinkBuddy AI Assistant",
            "features": [
                "Chat with AI",
                "RAG with ChromaDB",
                "Project context awareness",
                "Code snippet storage",
                "Conversation history"
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )
