# Complete Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 18+
- Firebase Project
- Google Gemini API Key

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies installed:**
- FastAPI - Web framework
- Firebase Admin - Database & Auth
- Google Generative AI - Gemini API
- ChromaDB - Vector database for RAG
- Sentence Transformers - Text embeddings
- WebSockets - Real-time communication

### 2. Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get Gemini API Key:**
- Visit: https://makersuite.google.com/app/apikey
- Sign in with Google account
- Create new API key
- Copy and paste into `.env` file

### 3. Firebase Configuration

Place your Firebase service account JSON file in:
```
backend/firebase-service-account.json
```

### 4. Start Backend Server

```bash
cd backend
python main.py
```

Server will run on: `http://127.0.0.2:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local` file in `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.2:8000
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend will run on: `http://localhost:3000`

## Features Overview

### 1. Team Chat
- Real-time messaging with WebSocket
- File sharing and reactions
- Message history

### 2. ThinkBuddy AI Assistant (RAG)
- Context-aware responses using team conversations
- Semantic search with ChromaDB
- Source attribution with relevance scores
- Powered by Google Gemini 2.0 Flash

### 3. Chat Summaries
- AI-generated conversation summaries
- Participant tracking
- Message statistics
- Powered by Google Gemini

### 4. Todo Management
- Team task tracking
- Priority levels
- Status updates

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Teams
- `GET /teams/` - Get user's teams
- `POST /teams/` - Create new team
- `GET /teams/{team_id}` - Get team details

### Messages
- `POST /messages/` - Send message
- `GET /messages/{team_id}` - Get team messages
- `WS /ws/{team_id}` - WebSocket connection

### AI Assistant (RAG)
- `POST /api/assistant/chat` - Chat with ThinkBuddy
- `GET /api/assistant/history` - Get conversation history
- `POST /api/assistant/clear-history` - Clear history
- `GET /api/assistant/health` - Health check

### Summaries
- `POST /summaries/generate` - Generate AI summary
- `GET /summaries/team/{team_id}` - Get team summaries
- `GET /summaries/{summary_id}` - Get specific summary
- `DELETE /summaries/{summary_id}` - Delete summary

### Todos
- `POST /todos/` - Create todo
- `GET /todos/team/{team_id}` - Get team todos
- `PUT /todos/{todo_id}` - Update todo
- `DELETE /todos/{todo_id}` - Delete todo

## How RAG Works

### Message Storage
When users send messages in team chats:
1. Message saved to Firestore
2. Message automatically indexed in ChromaDB vector database
3. Text embeddings generated using sentence-transformers

### Query Processing
When users ask ThinkBuddy questions:
1. Query converted to embedding
2. Semantic search in ChromaDB for relevant messages
3. Top 5 most relevant messages retrieved
4. Context + query sent to Gemini
5. Gemini generates contextual response
6. Response returned with source attribution

### Example Flow

```
User: "What did we discuss about the API?"
  ↓
ChromaDB Search: Find relevant messages about "API"
  ↓
Retrieved Context:
- Alice: "We need to implement REST API endpoints"
- Bob: "I suggest using FastAPI"
- Charlie: "API should handle authentication"
  ↓
Gemini Processing: Generate response using context
  ↓
Response: "Based on your team's discussions, you should 
implement REST API endpoints using FastAPI with 
authentication handling..."
  ↓
Sources Displayed:
- Alice (92% relevant)
- Bob (88% relevant)
- Charlie (85% relevant)
```

## Troubleshooting

### Backend Issues

**Error: GEMINI_API_KEY not found**
- Ensure `.env` file exists in `backend/` directory
- Check API key is correctly formatted
- Restart backend server

**Error: ChromaDB connection failed**
- ChromaDB is embedded, no external service needed
- Check disk space for vector database
- Try deleting `chroma_db/` folder and restart

**Error: Firebase initialization failed**
- Verify `firebase-service-account.json` exists
- Check file permissions
- Validate JSON format

### Frontend Issues

**Error: Cannot connect to backend**
- Verify backend is running on `http://127.0.0.2:8000`
- Check CORS settings in `main.py`
- Verify `.env.local` has correct API URL

**ThinkBuddy not responding**
- Check if user is logged in
- Verify Gemini API key is configured
- Check browser console for errors
- Ensure project/team is selected

**Sources not showing**
- Verify messages exist in vector database
- Check if RAG is enabled (`use_rag: true`)
- Ensure team context is selected

### Vector Database Issues

**No relevant results found**
- Check if messages are being indexed
- Verify team_id matches
- Ensure messages are text type
- Try with more messages in the team

**Slow response times**
- Reduce `n_results` parameter (default: 5)
- Check network latency
- Consider caching frequent queries

## Testing

### Test ThinkBuddy RAG

1. Create a team and send some messages
2. Click "ThinkBuddy" in sidebar
3. Select the team from dropdown
4. Ask a question about the team's conversations
5. Verify response includes sources with relevance scores

### Test Chat Summaries

1. Select a team with messages
2. Click "Summary" tab
3. Click "Generate Summary"
4. Wait for AI to process (3-8 seconds)
5. View structured summary with statistics

## Performance

- **Backend Response Time**: 50-200ms (without AI)
- **Vector Search**: 50-100ms
- **Gemini Generation**: 1-3 seconds
- **Total RAG Response**: 1.5-3.5 seconds
- **WebSocket Latency**: <50ms

## Security

- Firebase Authentication for all endpoints
- Team-scoped data access
- Vector database isolated by team
- API keys stored server-side only
- HTTPS recommended for production

## Production Deployment

### Backend
- Use production WSGI server (Gunicorn/Uvicorn)
- Set up environment variables securely
- Configure proper CORS origins
- Enable HTTPS
- Set up monitoring and logging

### Frontend
- Build for production: `npm run build`
- Deploy to Vercel/Netlify
- Configure environment variables
- Enable HTTPS
- Set up CDN for static assets

### Database
- Use Firebase production project
- Set up proper security rules
- Enable backups
- Monitor usage and quotas

## Support

For issues or questions:
1. Check this guide
2. Review error logs
3. Check API documentation
4. Verify environment configuration

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure environment variables
3. ✅ Start backend server
4. ✅ Start frontend server
5. ✅ Create account and login
6. ✅ Create a team
7. ✅ Send some messages
8. ✅ Try ThinkBuddy with RAG
9. ✅ Generate chat summaries
10. ✅ Explore all features

---

**Status**: ✅ All systems operational
**Version**: 1.0.0
**Last Updated**: January 2025
