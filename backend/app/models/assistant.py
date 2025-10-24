from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    project_context: Optional[str] = None
    use_rag: bool = True

class ChatResponse(BaseModel):
    response: str
    context_used: List[Dict[str, Any]] = []
    sources_count: int = 0
