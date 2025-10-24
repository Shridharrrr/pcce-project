import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os
from datetime import datetime

# Initialize ChromaDB client
chroma_client = chromadb.Client(Settings(
    anonymized_telemetry=False,
    allow_reset=True
))

# Get or create collection for messages
def get_messages_collection():
    """Get or create the messages collection"""
    return chroma_client.get_or_create_collection(
        name="team_messages",
        metadata={"description": "Team chat messages for RAG context"}
    )

def add_message_to_vector_db(message_id: str, content: str, metadata: Dict[str, Any]):
    """
    Add a message to the vector database
    
    Args:
        message_id: Unique message identifier
        content: Message content to embed
        metadata: Additional metadata (team_id, sender, timestamp, etc.)
    """
    try:
        collection = get_messages_collection()
        
        # Add document to collection
        collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[message_id]
        )
        
        return True
    except Exception as e:
        print(f"Error adding message to vector DB: {str(e)}")
        return False

def add_messages_batch(messages: List[Dict[str, Any]]):
    """
    Add multiple messages to vector database in batch
    
    Args:
        messages: List of message dictionaries with id, content, and metadata
    """
    try:
        collection = get_messages_collection()
        
        ids = []
        documents = []
        metadatas = []
        
        for msg in messages:
            if msg.get('content') and msg.get('message_type') == 'text':
                ids.append(msg['message_id'])
                documents.append(msg['content'])
                metadatas.append({
                    'team_id': msg.get('team_id', ''),
                    'sender_name': msg.get('sender_name', 'Unknown'),
                    'sender_id': msg.get('sender_id', ''),
                    'timestamp': msg.get('timestamp', ''),
                    'message_type': msg.get('message_type', 'text')
                })
        
        if ids:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
        return len(ids)
    except Exception as e:
        print(f"Error adding messages batch to vector DB: {str(e)}")
        return 0

def search_relevant_context(query: str, team_id: str = None, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for relevant messages based on query
    
    Args:
        query: User's question/query
        team_id: Optional team ID to filter results
        n_results: Number of results to return
        
    Returns:
        List of relevant messages with metadata
    """
    try:
        collection = get_messages_collection()
        
        # Build where filter
        where_filter = None
        if team_id:
            where_filter = {"team_id": team_id}
        
        # Query the collection
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        # Format results
        context_messages = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                distance = results['distances'][0][i] if results['distances'] else 0
                
                context_messages.append({
                    'content': doc,
                    'sender_name': metadata.get('sender_name', 'Unknown'),
                    'timestamp': metadata.get('timestamp', ''),
                    'team_id': metadata.get('team_id', ''),
                    'relevance_score': 1 - distance  # Convert distance to similarity score
                })
        
        return context_messages
    except Exception as e:
        print(f"Error searching vector DB: {str(e)}")
        return []

def delete_team_messages(team_id: str):
    """
    Delete all messages for a specific team
    
    Args:
        team_id: Team ID to delete messages for
    """
    try:
        collection = get_messages_collection()
        
        # Get all IDs for this team
        results = collection.get(
            where={"team_id": team_id}
        )
        
        if results and results['ids']:
            collection.delete(ids=results['ids'])
            return len(results['ids'])
        
        return 0
    except Exception as e:
        print(f"Error deleting team messages from vector DB: {str(e)}")
        return 0

def get_collection_stats():
    """Get statistics about the vector database"""
    try:
        collection = get_messages_collection()
        count = collection.count()
        
        return {
            "total_messages": count,
            "collection_name": "team_messages"
        }
    except Exception as e:
        print(f"Error getting collection stats: {str(e)}")
        return {"total_messages": 0, "collection_name": "team_messages"}
