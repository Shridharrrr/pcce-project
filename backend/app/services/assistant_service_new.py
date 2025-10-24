import google.generativeai as genai
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from app.services.vector_db_service import search_relevant_context, add_messages_batch
from app.services.firestore_service import get_team_messages

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AssistantService:
    """AI Assistant service using Gemini and ChromaDB for RAG"""
    
    def __init__(self):
        """Initialize the assistant service"""
        if not GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY not found")
        self.conversation_history = {}  # Store conversation history per user
    
    def search_relevant_context(query: str, team_id: str = None, n_results: int = 5) -> List[Dict[str, str]]:
        """Get conversation history for a user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def add_to_history(self, user_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 messages to avoid token limits
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
    
    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
    
    async def generate_response(
        self,
        user_id: str,
        message: str,
        project_context: Optional[str] = None,
        use_rag: bool = True
    ) -> Dict[str, Any]:
        """
        Generate AI response using Gemini with RAG (Retrieval Augmented Generation)
        
        Args:
            user_id: User identifier
            message: User's message
            project_context: Optional project/team context identifier
            use_rag: Whether to use RAG with vector database
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            if not GEMINI_API_KEY:
                raise Exception("GEMINI_API_KEY not configured")
            
            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Get conversation history
            history = self.get_conversation_history(user_id)
            
            # Retrieve relevant context from vector DB if RAG is enabled
            context_messages = []
            retrieved_sources = []
            context_text = ""
                            # Search for relevant messages from the team
                context_messages = search_relevant_context(
                    query=message,
                    team_id=project_context,
                    n_results=5
                )
                
                if context_messages:
                    context_text = "\n**Relevant Team Conversations:**\n"
                    for i, msg in enumerate(context_messages, 1):
                        sender = msg.get('sender_name', 'Unknown')
                        content = msg.get('content', '')
                        context_text += f"{i}. {sender}: {content[:150]}...\n"
                        
                        # Format sources for response
                        retrieved_sources.append({
                            "sender": sender,
                            "content": content[:100] + "...",
                            "timestamp": msg.get('timestamp', ''),
                            "relevance": round(msg.get('relevance_score', 0), 2)
                        })
            
            # Build the system prompt
            system_prompt = """You are ThinkBuddy, an intelligent AI assistant for team collaboration. You help with:
- Answering questions about team conversations
- Providing context from previous discussions
- Helping with project-related queries
- General assistance and information

You are helpful, concise, and provide actionable insights. When relevant context from team conversations is provided, use it to give accurate and personalized responses."""

            # Format conversation history
            history_text = ""
            if history:
                history_text = "\n**Recent Conversation:**\n"
                for msg in history[-5:]:  # Last 5 messages
                    role = "You" if msg['role'] == 'user' else "Assistant"
                    history_text += f"{role}: {msg['content']}\n"
            
            # Build final prompt
            full_prompt = f"""{system_prompt}

{history_text}

{context_text}

**User Question:** {message}

**Your Response:**"""

            # Generate response with Gemini
            response = model.generate_content(full_prompt)
            
            if not response or not response.text:
                raise Exception("Gemini returned empty response")
            
            assistant_response = response.text.strip()
            
            # Add to conversation history
            self.add_to_history(user_id, "user", message)
            self.add_to_history(user_id, "assistant", assistant_response)
            
            return {
                "response": assistant_response,
                "sources": retrieved_sources,
                "timestamp": datetime.now().isoformat(),
                "project_context": project_context or "general"
            }
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def add_project_knowledge(
        self,
        project_id: str,
        project_name: str,
        description: str,
        additional_info: Dict[str, Any] = None
    ) -> bool:
        """Add project knowledge - placeholder for future implementation"""
        return True
    
    def add_code_knowledge(
        self,
        code_id: str,
        code: str,
        language: str,
        description: str,
        project_id: Optional[str] = None
    ) -> bool:
        """Add code knowledge - placeholder for future implementation"""
        return True

# Global instance
assistant_service = AssistantService()
