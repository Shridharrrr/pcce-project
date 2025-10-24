import google.generativeai as genai
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from .chroma_service import chroma_service

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyArgXw1-BZKu-dXdbXr_CfNrPiB4eoUEcw")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AssistantService:
    """AI Assistant service using Gemini and ChromaDB"""
    
    def __init__(self):
        """Initialize the assistant service"""
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chroma = chroma_service
        self.conversation_history = {}  # Store conversation history per user
    
    def get_conversation_history(self, user_id: str) -> List[Dict[str, str]]:
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
            project_context: Optional project context identifier
            use_rag: Whether to use RAG with ChromaDB
            
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Get conversation history
            history = self.get_conversation_history(user_id)
            
            # Retrieve relevant context from ChromaDB if RAG is enabled
            context_data = ""
            retrieved_sources = []
            
            if use_rag:
                # Search for relevant information
                search_results = self.chroma.search_all(message, n_results=3)
                
                # Format context from search results
                context_parts = []
                
                # Add conversation context
                if search_results['conversations']['documents']:
                    context_parts.append("**Previous Conversations:**")
                    for i, (doc, meta) in enumerate(zip(
                        search_results['conversations']['documents'],
                        search_results['conversations']['metadatas']
                    )):
                        context_parts.append(f"{i+1}. {doc[:200]}...")
                        retrieved_sources.append({
                            "type": "conversation",
                            "content": doc[:100],
                            "metadata": meta
                        })
                
                # Add project context
                if search_results['projects']['documents']:
                    context_parts.append("\n**Project Information:**")
                    for i, (doc, meta) in enumerate(zip(
                        search_results['projects']['documents'],
                        search_results['projects']['metadatas']
                    )):
                        context_parts.append(f"{i+1}. {doc[:200]}...")
                        retrieved_sources.append({
                            "type": "project",
                            "content": doc[:100],
                            "metadata": meta
                        })
                
                # Add code snippets
                if search_results['code_snippets']['documents']:
                    context_parts.append("\n**Relevant Code:**")
                    for i, (doc, meta) in enumerate(zip(
                        search_results['code_snippets']['documents'],
                        search_results['code_snippets']['metadatas']
                    )):
                        context_parts.append(f"{i+1}. ```\n{doc[:300]}\n```")
                        retrieved_sources.append({
                            "type": "code",
                            "content": doc[:100],
                            "metadata": meta
                        })
                
                if context_parts:
                    context_data = "\n".join(context_parts)
            
            # Build the prompt
            system_prompt = """You are ThinkBuddy, an intelligent AI assistant designed to help with:
- Code explanation and debugging
- Project planning and best practices
- Technical questions and problem-solving
- Code review and suggestions
- General programming assistance

You are helpful, concise, and provide actionable insights. When relevant context is provided, use it to give more accurate and personalized responses."""

            # Format conversation history
            history_text = ""
            if history:
                history_text = "\n**Recent Conversation:**\n"
                for msg in history[-5:]:  # Last 5 messages
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    history_text += f"{role}: {msg['content']}\n"
            
            # Build final prompt
            full_prompt = f"""{system_prompt}

{history_text}

{context_data if context_data else ""}

{"**Project Context:** " + project_context if project_context else ""}

**User Question:** {message}

**Your Response:**"""

            # Generate response with Gemini
            response = self.model.generate_content(full_prompt)
            
            if not response or not response.text:
                raise Exception("Gemini returned empty response")
            
            assistant_response = response.text.strip()
            
            # Add to conversation history
            self.add_to_history(user_id, "user", message)
            self.add_to_history(user_id, "assistant", assistant_response)
            
            # Store conversation in ChromaDB for future RAG
            conversation_id = f"{user_id}_{datetime.now().timestamp()}"
            self.chroma.add_conversation(
                conversation_id=conversation_id,
                content=f"User: {message}\nAssistant: {assistant_response}",
                metadata={
                    "user_id": user_id,
                    "project_context": project_context or "general",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            return {
                "response": assistant_response,
                "sources": retrieved_sources if use_rag else [],
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
        """Add project knowledge to the vector database"""
        try:
            content = f"""Project: {project_name}
Description: {description}
{f"Additional Info: {additional_info}" if additional_info else ""}"""
            
            return self.chroma.add_project_context(
                project_id=project_id,
                content=content,
                metadata={
                    "project_name": project_name,
                    "description": description,
                    **(additional_info or {})
                }
            )
        except Exception as e:
            print(f"Error adding project knowledge: {str(e)}")
            return False
    
    def add_code_knowledge(
        self,
        code_id: str,
        code: str,
        language: str,
        description: str,
        project_id: Optional[str] = None
    ) -> bool:
        """Add code snippet to the knowledge base"""
        try:
            return self.chroma.add_code_snippet(
                snippet_id=code_id,
                code=code,
                metadata={
                    "language": language,
                    "description": description,
                    "project_id": project_id or "general"
                }
            )
        except Exception as e:
            print(f"Error adding code knowledge: {str(e)}")
            return False

# Global instance
assistant_service = AssistantService()
