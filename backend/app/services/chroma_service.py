import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any
from datetime import datetime

class ChromaDBService:
    """Service for managing ChromaDB vector database operations"""
    
    def __init__(self):
        """Initialize ChromaDB client and collections"""
        # Create persistent client
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Use sentence transformers for embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Initialize collections
        self.conversations_collection = self._get_or_create_collection("conversations")
        self.projects_collection = self._get_or_create_collection("projects")
        self.code_snippets_collection = self._get_or_create_collection("code_snippets")
    
    def _get_or_create_collection(self, name: str):
        """Get or create a collection with the given name"""
        try:
            return self.client.get_or_create_collection(
                name=name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error creating collection {name}: {str(e)}")
            raise
    
    def add_conversation(
        self, 
        conversation_id: str, 
        content: str, 
        metadata: Dict[str, Any]
    ) -> bool:
        """Add a conversation to the vector database"""
        try:
            self.conversations_collection.add(
                documents=[content],
                ids=[conversation_id],
                metadatas=[{
                    **metadata,
                    "timestamp": datetime.now().isoformat(),
                    "type": "conversation"
                }]
            )
            return True
        except Exception as e:
            print(f"Error adding conversation: {str(e)}")
            return False
    
    def add_project_context(
        self,
        project_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Add project context to the vector database"""
        try:
            self.projects_collection.add(
                documents=[content],
                ids=[project_id],
                metadatas=[{
                    **metadata,
                    "timestamp": datetime.now().isoformat(),
                    "type": "project"
                }]
            )
            return True
        except Exception as e:
            print(f"Error adding project context: {str(e)}")
            return False
    
    def add_code_snippet(
        self,
        snippet_id: str,
        code: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Add a code snippet to the vector database"""
        try:
            self.code_snippets_collection.add(
                documents=[code],
                ids=[snippet_id],
                metadatas=[{
                    **metadata,
                    "timestamp": datetime.now().isoformat(),
                    "type": "code"
                }]
            )
            return True
        except Exception as e:
            print(f"Error adding code snippet: {str(e)}")
            return False
    
    def search_conversations(
        self,
        query: str,
        n_results: int = 5,
        where: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search for relevant conversations"""
        try:
            results = self.conversations_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            return self._format_results(results)
        except Exception as e:
            print(f"Error searching conversations: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    def search_projects(
        self,
        query: str,
        n_results: int = 5,
        where: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search for relevant project contexts"""
        try:
            results = self.projects_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            return self._format_results(results)
        except Exception as e:
            print(f"Error searching projects: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    def search_code_snippets(
        self,
        query: str,
        n_results: int = 5,
        where: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search for relevant code snippets"""
        try:
            results = self.code_snippets_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            return self._format_results(results)
        except Exception as e:
            print(f"Error searching code snippets: {str(e)}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    def search_all(
        self,
        query: str,
        n_results: int = 3
    ) -> Dict[str, Any]:
        """Search across all collections"""
        conversations = self.search_conversations(query, n_results)
        projects = self.search_projects(query, n_results)
        code_snippets = self.search_code_snippets(query, n_results)
        
        return {
            "conversations": conversations,
            "projects": projects,
            "code_snippets": code_snippets
        }
    
    def _format_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format ChromaDB results"""
        if not results or not results.get('documents'):
            return {"documents": [], "metadatas": [], "distances": []}
        
        return {
            "documents": results['documents'][0] if results['documents'] else [],
            "metadatas": results['metadatas'][0] if results['metadatas'] else [],
            "distances": results['distances'][0] if results['distances'] else []
        }
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation from the database"""
        try:
            self.conversations_collection.delete(ids=[conversation_id])
            return True
        except Exception as e:
            print(f"Error deleting conversation: {str(e)}")
            return False
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project from the database"""
        try:
            self.projects_collection.delete(ids=[project_id])
            return True
        except Exception as e:
            print(f"Error deleting project: {str(e)}")
            return False
    
    def reset_database(self) -> bool:
        """Reset all collections (use with caution)"""
        try:
            self.client.reset()
            # Reinitialize collections
            self.conversations_collection = self._get_or_create_collection("conversations")
            self.projects_collection = self._get_or_create_collection("projects")
            self.code_snippets_collection = self._get_or_create_collection("code_snippets")
            return True
        except Exception as e:
            print(f"Error resetting database: {str(e)}")
            return False

# Global instance
chroma_service = ChromaDBService()
