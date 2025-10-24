import google.generativeai as genai
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from app.services.vector_db_service import search_relevant_context, add_messages_batch
from app.services.firestore_service import (
    get_team_messages, 
    save_assistant_message, 
    get_assistant_chat_history,
    clear_assistant_chat_history
)

# Load environment variables
load_dotenv()

# Configure Gemini - use env variable or fallback to hardcoded key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyArgXw1-BZKu-dXdbXr_CfNrPiB4eoUEcw"
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AssistantService:
    """AI Assistant service using Gemini and ChromaDB for RAG"""
    
    def __init__(self):
        """Initialize the assistant service"""
        if not GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY not found")
        self.conversation_history = {}  # Store conversation history per user per project: {user_id: {project_id: [messages]}}
    
    def get_conversation_history(self, user_id: str, project_context: str = "general") -> List[Dict[str, str]]:
        """Get conversation history for a user and project - loads from Firestore if not in memory"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = {}
        
        if project_context not in self.conversation_history[user_id]:
            # Load from Firestore
            try:
                stored_messages = get_assistant_chat_history(user_id, project_context, limit=50)
                self.conversation_history[user_id][project_context] = stored_messages
            except Exception as e:
                print(f"Error loading chat history from Firestore: {e}")
                self.conversation_history[user_id][project_context] = []
        return self.conversation_history[user_id][project_context]
    
    def add_to_history(self, user_id: str, role: str, content: str, sources: List[Dict[str, Any]] = None, project_context: str = "general"):
        """Add a message to conversation history and persist to Firestore"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = {}
        
        if project_context not in self.conversation_history[user_id]:
            self.conversation_history[user_id][project_context] = []
        
        message_data = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "sources": sources or [],
            "project_context": project_context
        }
        
        self.conversation_history[user_id][project_context].append(message_data)
        
        # Persist to Firestore
        try:
            save_assistant_message(user_id, message_data, project_context)
        except Exception as e:
            print(f"Error persisting message to Firestore: {e}")
        
        # Keep only last 50 messages in memory to avoid token limits
        if len(self.conversation_history[user_id][project_context]) > 50:
            self.conversation_history[user_id][project_context] = self.conversation_history[user_id][project_context][-50:]
    
    def clear_history(self, user_id: str, project_context: str = None):
        """Clear conversation history for a user from memory and Firestore"""
        if project_context:
            # Clear specific project history
            if user_id in self.conversation_history and project_context in self.conversation_history[user_id]:
                self.conversation_history[user_id][project_context] = []
        else:
            # Clear all project histories
            if user_id in self.conversation_history:
                self.conversation_history[user_id] = {}
        
        # Clear from Firestore
        try:
            clear_assistant_chat_history(user_id, project_context)
        except Exception as e:
            print(f"Error clearing chat history from Firestore: {e}")
    
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
            
            # Normalize project context
            normalized_context = project_context or "general"
            
            # Get conversation history for this specific project
            history = self.get_conversation_history(user_id, normalized_context)
            
            # Retrieve relevant context from vector DB if RAG is enabled
            context_messages = []
            retrieved_sources = []
            
            # Build context from RAG
            context_data = ""
            if use_rag:
                team_messages = []
                if project_context:
                    team_messages = get_team_messages(project_context)

                # Search for relevant messages from the team (or all teams if no context)
                # This searches ALL users' messages in the team, not just current user
                print(f"🔍 Searching vector DB for: '{message}' in team: {project_context}")
                context_messages = search_relevant_context(
                    query=message,
                    team_id=project_context,  # If None, searches across all teams
                    n_results=10  # Increased to get more context from all users
                )
                print(f"📊 Found {len(context_messages)} relevant messages")
                
                # Format sources for response and build context
                if context_messages:
                    context_parts = ["\n**Relevant Team Messages from All Team Members:**"]
                    for i, msg in enumerate(context_messages, 1):
                        sender = msg.get("sender_name", "Unknown")
                        content = msg.get("content", "")
                        timestamp = msg.get("timestamp", "")
                
                        retrieved_sources.append({
                            "sender": sender,
                            "content": content[:100] + "..." if len(content) > 100 else content,
                            "timestamp": timestamp,
                            "relevance": round(msg.get("relevance_score", 0), 2),
                        })
                
                        # Include full context for better AI understanding
                        context_parts.append(f"{i}. [{sender}] ({timestamp}): {content[:500]}")
                
                    context_data = "\n".join(context_parts)
                else:
                    context_data = "No relevant team messages found."
                
                # Build the system prompt
                system_prompt = """You are ThinkBuddy — an intelligent AI assistant designed to help with:
                - Code explanation and debugging
                - Project planning and best practices
                - Technical questions and problem-solving
                - Code review and suggestions
                - General programming assistance
                - Project summarization and analysis
                
                You are helpful, concise, and provide actionable insights.
                
                IMPORTANT:
                When relevant team messages are provided below, they are from ALL team members — not just the current user.
                You MUST analyze these messages collectively to give accurate, comprehensive, and context-aware responses
                based on the entire project’s data. Avoid generic replies when specific context is available.
                
                For project summaries, analyze all team messages and provide clear insights about:
                - What the team has discussed
                - Decisions made
                - Current project status
                - Key contributions from each team member
                - Overall progress and direction
                """
                
                # Format recent conversation history (limit to last 5 messages)
                history_text = ""
                if history:
                    history_text = "\n**Recent Conversation:**\n"
                    for msg in history[-5:]:
                        role = "User" if msg["role"] == "user" else "Assistant"
                        history_text += f"{role}: {msg['content']}\n"
                
                # Build the final prompt for the AI model
                full_prompt = f"""
                {system_prompt}
                
                **Team Messages (All Members):**
                {team_context if team_context else "No messages available."}
                
                **Relevant Context:**
                {context_data}
                
                {history_text}
                
                **User Question:** {message}
                
                **Your Response:**
                """
                


            # Generate response with Gemini
            response = model.generate_content(full_prompt)
            
            if not response or not response.text:
                raise Exception("Gemini returned empty response")
            
            assistant_response = response.text.strip()
            
            # Add to conversation history with sources and project context
            self.add_to_history(user_id, "user", message, sources=[], project_context=normalized_context)
            self.add_to_history(user_id, "assistant", assistant_response, sources=retrieved_sources, project_context=normalized_context)
            
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
            
            # Add to vector database
            from app.services.vector_db_service import add_message_to_vector_db
            return add_message_to_vector_db(
                message_id=f"project_{project_id}",
                content=content,
                metadata={
                    "team_id": project_id,
                    "sender_name": "System",
                    "message_type": "project_info",
                    "project_name": project_name,
                    "timestamp": datetime.now().isoformat(),
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
            content = f"""Code Snippet ({language}):
{description}

```{language}
{code}
```"""
            
            from app.services.vector_db_service import add_message_to_vector_db
            return add_message_to_vector_db(
                message_id=f"code_{code_id}",
                content=content,
                metadata={
                    "team_id": project_id or "general",
                    "sender_name": "System",
                    "message_type": "code_snippet",
                    "language": language,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            print(f"Error adding code knowledge: {str(e)}")
            return False

# Global instance
assistant_service = AssistantService()
