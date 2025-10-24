# ThinkBuddy AI Assistant - Quick Start Guide

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure API Key
Edit `backend/.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### Step 3: Start the Server
```bash
cd backend
python main.py
```

## ✅ Verify Installation

Run the installation checker:
```bash
cd backend
python install_assistant.py
```

## 🎯 What You Get

### 1. **AI Chat Interface**
- Natural language conversations
- Project-specific context awareness
- Conversation history

### 2. **RAG (Retrieval Augmented Generation)**
- Searches previous conversations
- Retrieves relevant project info
- Finds related code snippets

### 3. **Knowledge Base**
- Store project documentation
- Save code snippets
- Build contextual knowledge

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/assistant/chat` | POST | Chat with AI |
| `/api/assistant/history` | GET | Get chat history |
| `/api/assistant/clear-history` | POST | Clear history |
| `/api/assistant/knowledge/project` | POST | Add project info |
| `/api/assistant/knowledge/code` | POST | Add code snippet |
| `/api/assistant/health` | GET | Health check |

## 💡 Usage Examples

### Chat Request
```javascript
const response = await fetch('http://127.0.0.2:8000/api/assistant/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    message: "Explain React hooks",
    project_context: "webdev",
    use_rag: true
  })
});
```

### Add Project Knowledge
```javascript
await fetch('http://127.0.0.2:8000/api/assistant/knowledge/project', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    project_id: "my-project",
    project_name: "My Web App",
    description: "A React-based web application",
    additional_info: {
      tech_stack: ["React", "Node.js", "MongoDB"]
    }
  })
});
```

## 🏗️ Architecture

```
Frontend (React)
    ↓
Backend API (FastAPI)
    ↓
Assistant Service (Gemini + ChromaDB)
    ↓
[ChromaDB Vector DB] ← RAG Search
    ↓
Gemini API → AI Response
```

## 📁 Files Created

### Backend
- `app/services/chroma_service.py` - Vector database operations
- `app/services/assistant_service.py` - AI logic with Gemini
- `app/routes/assistant_routes.py` - API endpoints
- `install_assistant.py` - Installation checker

### Frontend
- `ThinkBuddyAssistant.jsx` - Updated with API integration

### Documentation
- `AI_ASSISTANT_SETUP.md` - Detailed setup guide
- `ASSISTANT_QUICKSTART.md` - This file

## 🔧 Configuration

### ChromaDB
- **Location**: `backend/chroma_db/`
- **Embedding Model**: all-MiniLM-L6-v2
- **Similarity**: Cosine

### Gemini
- **Model**: gemini-2.0-flash
- **API Key**: From environment variable

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if dependencies are installed
pip list | grep -E "chromadb|google-generativeai|sentence-transformers"

# Reinstall if needed
pip install -r requirements.txt
```

### API returns 401 Unauthorized
- Ensure you're logged in
- Check if token is in localStorage
- Verify token is sent in Authorization header

### ChromaDB errors
```bash
# Delete and recreate database
rm -rf backend/chroma_db
# Restart server - it will recreate automatically
```

## 📊 Testing

### Test the API
```bash
# Health check
curl http://127.0.0.2:8000/api/assistant/health

# Check API docs
# Open: http://127.0.0.2:8000/docs
```

### Test from Frontend
1. Open the application
2. Navigate to ThinkBuddy Assistant
3. Select a project context
4. Send a test message: "Hello, can you help me?"

## 🎨 Features in Action

### Context-Aware Responses
- Select "Web Development" → Get web-specific advice
- Select "AI & Machine Learning" → Get AI-specific help
- Select "General" → Get general programming help

### RAG in Action
1. Have a conversation about React
2. Later ask: "What did we discuss about React?"
3. The assistant retrieves previous context automatically

### Knowledge Building
1. Add your project info via API
2. Add code snippets you use frequently
3. Assistant references them in future conversations

## 🔐 Security

- ✅ Authentication required for all endpoints
- ✅ User-isolated conversations
- ✅ API key stored securely in .env
- ✅ CORS configured for frontend

## 📈 Next Steps

1. **Start using the assistant** through the frontend
2. **Add project knowledge** for better responses
3. **Store code snippets** you reference often
4. **Explore API docs** at http://127.0.0.2:8000/docs

## 💬 Support

For detailed information, see `AI_ASSISTANT_SETUP.md`

---

**Ready to go!** 🎉 Start the backend server and begin chatting with ThinkBuddy!
