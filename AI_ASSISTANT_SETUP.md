# ThinkBuddy AI Assistant Setup Guide

## Overview
ThinkBuddy is an AI-powered assistant integrated into your workspace management system. It uses:
- **Gemini 2.0 Flash** for natural language understanding and generation
- **ChromaDB** as a vector database for Retrieval Augmented Generation (RAG)
- **Sentence Transformers** for embedding generation

## Features

### 1. **Intelligent Chat Interface**
- Natural conversation with context awareness
- Project-specific responses based on selected context
- Conversation history management

### 2. **RAG (Retrieval Augmented Generation)**
- Stores and retrieves relevant information from:
  - Previous conversations
  - Project documentation
  - Code snippets
- Provides context-aware responses using ChromaDB vector search

### 3. **Knowledge Base Management**
- Add project information to the knowledge base
- Store code snippets for future reference
- Automatic conversation indexing

## Installation

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

The following packages will be installed:
- `chromadb` - Vector database
- `sentence-transformers` - Embedding generation
- `google-generativeai` - Gemini API client

2. **Environment Configuration**
Make sure your `.env` file contains:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Start the Backend Server**
```bash
python main.py
```

The server will start on `http://127.0.0.2:8000`

### Frontend Setup

The frontend is already configured to connect to the backend API. No additional setup required.

## API Endpoints

### Chat Endpoint
**POST** `/api/assistant/chat`

Request:
```json
{
  "message": "Explain this code snippet",
  "project_context": "webdev",
  "use_rag": true
}
```

Response:
```json
{
  "response": "AI generated response...",
  "sources": [
    {
      "type": "conversation",
      "content": "Previous relevant conversation...",
      "metadata": {...}
    }
  ],
  "timestamp": "2024-01-01T12:00:00",
  "project_context": "webdev"
}
```

### Clear History
**POST** `/api/assistant/clear-history`

Clears conversation history for the current user.

### Get History
**GET** `/api/assistant/history`

Returns conversation history for the current user.

### Add Project Knowledge
**POST** `/api/assistant/knowledge/project`

Request:
```json
{
  "project_id": "proj_123",
  "project_name": "My Web App",
  "description": "A full-stack web application...",
  "additional_info": {
    "tech_stack": ["React", "Node.js", "MongoDB"]
  }
}
```

### Add Code Knowledge
**POST** `/api/assistant/knowledge/code`

Request:
```json
{
  "code_id": "code_123",
  "code": "function example() { return 'Hello'; }",
  "language": "javascript",
  "description": "Example function",
  "project_id": "proj_123"
}
```

### Health Check
**GET** `/api/assistant/health`

Check if the assistant service is operational.

## Usage

### Using the Chat Interface

1. **Select Project Context**
   - Choose a project from the dropdown to get context-aware responses
   - Select "General" for general programming questions

2. **Ask Questions**
   - Type your question in the input field
   - Press Enter to send (Shift+Enter for new line)
   - Use predefined prompts for quick access

3. **View Responses**
   - AI responses appear with relevant sources (if RAG is enabled)
   - Conversation history is maintained automatically

### Adding Knowledge to the Database

You can programmatically add knowledge to enhance the assistant's responses:

```javascript
// Add project knowledge
const addProjectKnowledge = async (projectData) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://127.0.0.2:8000/api/assistant/knowledge/project', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(projectData)
  });
  return response.json();
};

// Add code snippet
const addCodeSnippet = async (codeData) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://127.0.0.2:8000/api/assistant/knowledge/code', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(codeData)
  });
  return response.json();
};
```

## Architecture

### Backend Components

1. **ChromaDB Service** (`app/services/chroma_service.py`)
   - Manages vector database operations
   - Handles embeddings with sentence-transformers
   - Provides search functionality across collections

2. **Assistant Service** (`app/services/assistant_service.py`)
   - Integrates Gemini API for response generation
   - Implements RAG using ChromaDB
   - Manages conversation history

3. **Assistant Routes** (`app/routes/assistant_routes.py`)
   - Exposes REST API endpoints
   - Handles authentication
   - Validates requests

### Data Flow

```
User Input → Frontend → Backend API → Assistant Service
                                            ↓
                                    ChromaDB Search (RAG)
                                            ↓
                                    Gemini API (Response Generation)
                                            ↓
                                    Store in ChromaDB
                                            ↓
Frontend ← Backend API ← Response with Sources
```

## ChromaDB Collections

### 1. Conversations Collection
Stores chat history for RAG:
- User messages and assistant responses
- Timestamps and user IDs
- Project context metadata

### 2. Projects Collection
Stores project information:
- Project descriptions
- Technical details
- Additional metadata

### 3. Code Snippets Collection
Stores code examples:
- Code content
- Programming language
- Descriptions and tags

## Configuration

### ChromaDB Settings
The database is stored in `./chroma_db` directory with:
- Persistent storage
- Cosine similarity for vector search
- Sentence transformer embeddings (all-MiniLM-L6-v2)

### Gemini Settings
- Model: `gemini-2.0-flash`
- Temperature: Default
- Max tokens: Automatic

## Troubleshooting

### Issue: "Failed to get response from assistant"
**Solution:** 
- Check if backend server is running
- Verify GEMINI_API_KEY is set correctly
- Check network connectivity

### Issue: ChromaDB initialization error
**Solution:**
- Ensure write permissions for `./chroma_db` directory
- Delete `./chroma_db` folder and restart server to reset

### Issue: Slow responses
**Solution:**
- First request may be slow due to model loading
- Subsequent requests should be faster
- Consider reducing `n_results` in RAG searches

## Best Practices

1. **Project Context**
   - Always select appropriate project context for better responses
   - Add project knowledge before asking project-specific questions

2. **Knowledge Base**
   - Regularly update project information
   - Add code snippets that you frequently reference
   - Keep descriptions clear and concise

3. **Conversation Management**
   - Clear history periodically to maintain relevance
   - Use specific questions for better responses

## Security Notes

- API endpoints require authentication (Bearer token)
- Gemini API key should be kept secure in `.env` file
- User conversations are isolated by user ID
- ChromaDB data is stored locally

## Future Enhancements

Potential improvements:
- [ ] Multi-modal support (images, files)
- [ ] Advanced code analysis
- [ ] Integration with version control
- [ ] Team knowledge sharing
- [ ] Custom embedding models
- [ ] Response streaming

## Support

For issues or questions:
1. Check the logs in the backend console
2. Verify API endpoint responses
3. Test with `/api/assistant/health` endpoint
4. Review ChromaDB collections for data integrity
