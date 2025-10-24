# ThinkBuddy AI Assistant - Troubleshooting Guide

## Error: "Failed to get response from assistant"

This error occurs when the frontend cannot communicate with the backend API. Follow these steps to diagnose and fix:

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Expected packages:**
- chromadb
- sentence-transformers
- google-generativeai
- fastapi
- uvicorn

### Step 2: Run Diagnostic Test

```bash
cd backend
python test_assistant.py
```

This will check:
- ✅ All required packages are installed
- ✅ ChromaDB is working
- ✅ Gemini API is accessible
- ✅ Assistant service is functional

### Step 3: Start Backend Server

```bash
cd backend
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.2:8000
```

### Step 4: Test API Endpoint

Open a new terminal and run:

```bash
curl http://127.0.0.2:8000/api/assistant/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "ThinkBuddy AI Assistant",
  "features": [...]
}
```

### Step 5: Check Browser Console

Open browser DevTools (F12) and check the Console tab for error details.

**Common errors and solutions:**

#### Error: "Failed to fetch" or "Network error"
**Cause:** Backend server is not running  
**Solution:** Start the backend server (Step 3)

#### Error: "401 Unauthorized"
**Cause:** Not logged in or invalid token  
**Solution:** 
- Log out and log back in
- Check if token exists: `localStorage.getItem('token')`

#### Error: "500 Internal Server Error"
**Cause:** Backend error (check server logs)  
**Solution:** Look at the backend terminal for error details

#### Error: "CORS policy"
**Cause:** CORS configuration issue  
**Solution:** Backend already has CORS enabled, but verify in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Common Issues and Solutions

### Issue 1: ChromaDB Import Error

**Error:**
```
ImportError: cannot import name 'chromadb'
```

**Solution:**
```bash
pip install chromadb
```

If that fails:
```bash
pip install --upgrade pip
pip install chromadb --no-cache-dir
```

### Issue 2: Sentence Transformers Download

**Error:**
```
Downloading model 'all-MiniLM-L6-v2'...
```

**Note:** First run will download the embedding model (~80MB). This is normal and only happens once.

**If download fails:**
- Check internet connection
- Try manually: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"`

### Issue 3: Gemini API Error

**Error:**
```
google.api_core.exceptions.PermissionDenied: 403 API key not valid
```

**Solution:**
1. Get a valid Gemini API key from: https://makersuite.google.com/app/apikey
2. Update in `backend/.env`:
   ```env
   GEMINI_API_KEY=your_actual_api_key
   ```
3. Or update in `backend/app/services/gemini_service.py` (line 9)

### Issue 4: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in main.py:
uvicorn.run(app, host="127.0.0.2", port=8001)
```

### Issue 5: ChromaDB Permission Error

**Error:**
```
PermissionError: [Errno 13] Permission denied: './chroma_db'
```

**Solution:**
```bash
# Delete and recreate
rm -rf chroma_db
# Or on Windows
rmdir /s chroma_db

# Restart server - it will recreate automatically
```

### Issue 6: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'app.services.assistant_service'
```

**Solution:**
Ensure you're running from the correct directory:
```bash
cd backend
python main.py
```

Not from the project root.

---

## Quick Fixes Checklist

- [ ] Backend server is running (`python main.py`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Gemini API key is configured
- [ ] Port 8000 is not blocked by firewall
- [ ] User is logged in (token in localStorage)
- [ ] Browser console shows actual error message
- [ ] Backend terminal shows no errors

---

## Testing the Complete Flow

### 1. Test Backend Health
```bash
curl http://127.0.0.2:8000/health
```

### 2. Test Assistant Health
```bash
curl http://127.0.0.2:8000/api/assistant/health
```

### 3. Test Chat (requires auth token)
```bash
curl -X POST http://127.0.0.2:8000/api/assistant/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "Hello", "use_rag": false}'
```

### 4. Test from Frontend
1. Open application
2. Navigate to ThinkBuddy Assistant
3. Open browser console (F12)
4. Send message: "Hello"
5. Check console for request/response

---

## Debug Mode

### Enable Verbose Logging

Add to `backend/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Request Details

In `ThinkBuddyAssistant.jsx`, the error now shows:
- HTTP status code
- Error message from backend
- Network connectivity issues

Look for the error message in the chat interface - it will now show the actual error.

---

## Still Having Issues?

### Collect Debug Information

1. **Backend logs:**
   - Copy the terminal output when you start the server
   - Copy any error messages

2. **Browser console:**
   - Open DevTools (F12)
   - Go to Console tab
   - Copy the error messages

3. **Test results:**
   ```bash
   python test_assistant.py > test_results.txt
   ```

4. **Network tab:**
   - Open DevTools → Network tab
   - Try sending a message
   - Check the request to `/api/assistant/chat`
   - Look at Status, Headers, Response

### Verify Installation

```bash
cd backend
python install_assistant.py
```

This will check all components and report any issues.

---

## Environment Verification

Create a test file `backend/verify_env.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("Environment Variables:")
print(f"GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY', 'NOT SET')[:20]}...")

print("\nPython Path:")
import sys
print(sys.executable)

print("\nInstalled Packages:")
import pkg_resources
for package in ['chromadb', 'google-generativeai', 'sentence-transformers', 'fastapi']:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"✅ {package}: {version}")
    except:
        print(f"❌ {package}: NOT INSTALLED")
```

Run: `python verify_env.py`

---

## Contact & Support

If you've tried all the above and still have issues:

1. Check the detailed setup guide: `AI_ASSISTANT_SETUP.md`
2. Review the quick start: `ASSISTANT_QUICKSTART.md`
3. Run the diagnostic: `python test_assistant.py`
4. Check API docs: http://127.0.0.2:8000/docs (when server is running)
