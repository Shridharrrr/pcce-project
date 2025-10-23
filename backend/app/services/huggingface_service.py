import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

HUGGINGFACE_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def generate_summary(messages: List[Dict[str, Any]], max_length: int = 150) -> str:
    """
    Generate a summary of chat messages using Hugging Face inference API
    
    Args:
        messages: List of message dictionaries with 'content', 'sender_name', etc.
        max_length: Maximum length of the summary
        
    Returns:
        Generated summary text
    """
    if not HUGGINGFACE_API_KEY:
        raise Exception("HUGGINGFACE_API_KEY not found in environment variables")
    
    if not messages:
        return "No messages to summarize."
    
    # Prepare the text for summarization
    # Format: "Sender: Message content"
    chat_text = "\n".join([
        f"{msg.get('sender_name', 'Unknown')}: {msg.get('content', '')}"
        for msg in messages
        if msg.get('content') and msg.get('message_type') == 'text'
    ])
    
    if not chat_text.strip():
        return "No text messages to summarize."
    
    # Limit input text length (BART has a max token limit)
    max_input_chars = 5000
    if len(chat_text) > max_input_chars:
        chat_text = chat_text[:max_input_chars] + "..."
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": chat_text,
        "parameters": {
            "max_length": max_length,
            "min_length": 30,
            "do_sample": False
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Handle different response formats
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get("summary_text", "")
        elif isinstance(result, dict):
            summary = result.get("summary_text", "")
        else:
            summary = str(result)
        
        return summary if summary else "Unable to generate summary."
        
    except requests.exceptions.Timeout:
        raise Exception("Hugging Face API request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling Hugging Face API: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")


def generate_summary_with_key_points(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a comprehensive summary with key points
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Dictionary with summary and metadata
    """
    summary_text = generate_summary(messages, max_length=200)
    
    # Extract some basic statistics
    total_messages = len(messages)
    text_messages = [m for m in messages if m.get('message_type') == 'text']
    unique_senders = set(m.get('sender_name', 'Unknown') for m in messages)
    
    return {
        "summary": summary_text,
        "total_messages": total_messages,
        "text_messages_count": len(text_messages),
        "participants": list(unique_senders),
        "participant_count": len(unique_senders)
    }
