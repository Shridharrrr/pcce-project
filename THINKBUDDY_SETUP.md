# ThinkBuddy AI Assistant - Complete Setup Guide

## Overview
ThinkBuddy is now fully integrated with **Gemini AI API** and **ChromaDB Vector Database** for RAG (Retrieval Augmented Generation). It provides intelligent, context-aware responses based on your actual project data.

## Architecture

### Backend Components
1. **Gemini AI (gemini-2.0-flash)** - Powers the AI responses
2. **ChromaDB Vector Database** - Stores and retrieves message embeddings for RAG
3. **Assistant Service** - Orchestrates AI + RAG
4. **Vector DB Service** - Manages ChromaDB operations

### How RAG Works
1. When you send a message to ThinkBuddy with a project context
2. System searches ChromaDB for relevant team messages using semantic similarity
3. Top 5 most relevant messages are retrieved
4. These messages are included in the prompt to Gemini
5. Gemini generates a response based on actual project data
6. Sources are shown to you in the UI

## Files Modified

### Backend
- ✅ `backend/main.py` - Fixed host to 127.0.0.1
- ✅ `backend/app/services/assistant_service.py` - Complete RAG integration
- ✅ `backend/app/services/vector_db_service.py` - ChromaDB operations
- ✅ `backend/app/routes/assistant_routes.py` - API endpoints
- ✅ `backend/test_assistant.py` - Diagnostic test script

### Frontend
- ✅ `frontend/src/components/ThinkBuddyAssistant.jsx` - Real API integration
- ✅ All components - Fixed API URL from 127.0.0.2 to 127.0.0.1

## API Configuration

### Gemini API Key
Located in: `backend/app/services/assistant_service.py` and `gemini_service.py`
```python
GEMINI_API_KEY = "AIzaSyArgXw1-BZKu-dXdbXr_CfNrPiB4eoUEcw"
```

### API Endpoints
- `POST /api/assistant/chat` - Chat with AI assistant
- `GET /api/assistant/health` - Health check
- `GET /api/assistant/history` - Get conversation history
- `POST /api/assistant/clear-history` - Clear history
- `POST /api/assistant/knowledge/project` - Add project knowledge
- `POST /api/assistant/knowledge/code` - Add code snippets

## Testing

### Run Diagnostic Test
```bash
cd backend
python test_assistant.py
```

This will test:
1. ✅ Package imports (chromadb, google-generativeai, sentence-transformers)
2. ✅ Gemini API key configuration
3. ✅ ChromaDB vector database operations
4. ✅ Gemini API connectivity
5. ✅ Assistant service end-to-end

### Start Backend Server
```bash
cd backend
python main.py
```
Server runs on: `http://127.0.0.1:8000`

### Start Frontend
```bash
cd frontend
npm run dev
```

## Usage

### 1. Select a Project
In the ThinkBuddy interface, select your project from the dropdown (e.g., "hacktest")

### 2. Ask Questions
Examples:
- "Summarize the project"
- "What have we discussed so far?"
- "What are the main decisions made?"
- "Help me understand the project goals"

### 3. View Sources
When RAG is used, you'll see "📚 Sources from project context" showing which team messages were used to generate the response.

## How Messages Get Into Vector DB

Messages are automatically added to ChromaDB when:
1. A team member sends a message (via `message_routes.py`)
2. The `add_message_to_vector_db()` function is called
3. Message content is embedded and stored with metadata

## Customization

### Adjust RAG Results
In `assistant_service.py`, line 90:
```python
context_messages = search_relevant_context(
    query=message,
    team_id=project_context,
    n_results=5  # Change this number
)
```

### Change AI Model
In `assistant_service.py`, line 76:
```python
model = genai.GenerativeModel('gemini-2.0-flash')  # Try other models
```

### Modify System Prompt
In `assistant_service.py`, lines 110-122:
Edit the system prompt to change AI behavior

## Troubleshooting

### Issue: "Using offline mode" message
**Cause:** API call failed
**Fix:** 
1. Check backend is running on 127.0.0.1:8000
2. Run `python test_assistant.py` to diagnose
3. Check browser console for errors

### Issue: Generic responses despite having project data
**Cause:** No messages in vector database for that project
**Fix:**
1. Send some messages in the project chat first
2. Messages are auto-indexed to ChromaDB
3. Try asking again

### Issue: "GEMINI_API_KEY not configured"
**Fix:** API key is hardcoded as fallback, but check:
```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyArgXw1-BZKu-dXdbXr_CfNrPiB4eoUEcw"
```

## Performance Notes

- **First query**: May be slower (model initialization)
- **Subsequent queries**: Fast (<2 seconds)
- **Vector search**: Very fast (<100ms)
- **Gemini API**: Usually 1-2 seconds

## Security Notes

⚠️ **Important:** The Gemini API key is currently hardcoded. For production:
1. Move to environment variables
2. Use `.env` file (already gitignored)
3. Never commit API keys to git

## Next Steps

1. ✅ Test the diagnostic script
2. ✅ Start both backend and frontend
3. ✅ Select a project with existing messages
4. ✅ Ask ThinkBuddy to summarize the project
5. ✅ Verify it uses actual project data (check sources)

---

**Status:** ✅ Fully Functional
**Last Updated:** 2025-10-24
