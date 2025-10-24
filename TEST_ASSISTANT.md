# Testing ThinkBuddy AI Assistant - Step by Step

## ✅ The Fix Applied

**Problem:** The assistant was looking for token in `localStorage`, but your app uses Firebase Authentication which provides tokens via `user.getIdToken()`.

**Solution:** Updated the assistant to get the Firebase ID token directly from the authenticated user object.

## 🧪 How to Test

### Step 1: Start Backend Server

```bash
cd backend
venv\Scripts\activate
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.2:8000
```

### Step 2: Start Frontend

```bash
cd frontend
npm run dev
```

### Step 3: Log In First! (IMPORTANT)

1. Open your application in the browser
2. **Log in with your email/password or Google**
3. Wait for login to complete
4. You should see your user profile/name

### Step 4: Navigate to ThinkBuddy Assistant

1. Go to the ThinkBuddy Assistant page
2. You should see:
   - ✅ No yellow warning banner
   - ✅ Input field is enabled
   - ✅ Predefined prompts are clickable

### Step 5: Send a Test Message

1. Type: "Hello, can you help me?"
2. Press Enter or click Send
3. Wait for response

**Expected behavior:**
- Message appears in chat
- "Typing..." indicator shows
- AI response appears after a few seconds

## 🔍 Debugging

### If you see the yellow warning banner:

**Check 1: Are you logged in?**
- Look for your user profile/avatar in the app
- Check browser console: `console.log(user)` should show user object

**Check 2: Is Firebase initialized?**
- Check browser console for Firebase errors
- Verify `firebase.js` config is correct

### If you get authentication error:

**Check backend logs:**
Look at the terminal where you ran `python main.py`. You should see:
```
Authentication error: [error details]
```

**Common errors:**

1. **"Wrong number of segments in token"**
   - Token is null or invalid
   - User is not logged in
   - **FIX:** Log in first!

2. **"Firebase ID token has expired"**
   - Token expired (happens after 1 hour)
   - **FIX:** Refresh the page to get new token

3. **"Failed to verify token"**
   - Firebase config mismatch
   - **FIX:** Check backend firebase-service-account.json

### If backend returns 500 error:

**Check backend terminal for:**
- ChromaDB errors
- Gemini API errors
- Import errors

**Run diagnostic:**
```bash
cd backend
python test_assistant.py
```

## 📋 Quick Checklist

Before testing, ensure:

- [ ] Backend server is running (`python main.py`)
- [ ] Frontend is running (`npm run dev`)
- [ ] You are **LOGGED IN** to the application
- [ ] You can see your user profile/name in the app
- [ ] No errors in browser console (F12)
- [ ] No errors in backend terminal

## 🎯 What Should Work Now

1. **Login Detection** ✅
   - Warning banner appears only when not logged in
   - Input disabled when not logged in

2. **Token Retrieval** ✅
   - Gets Firebase ID token from authenticated user
   - No more "null" token errors

3. **API Communication** ✅
   - Sends proper Authorization header
   - Backend validates Firebase token
   - Returns AI response

4. **Error Handling** ✅
   - Shows actual error messages
   - Provides helpful feedback

## 🚀 Expected Flow

```
1. User logs in with Firebase Auth
   ↓
2. Firebase provides authenticated user object
   ↓
3. User navigates to ThinkBuddy
   ↓
4. Component checks: user exists? → Yes ✅
   ↓
5. User sends message
   ↓
6. Get Firebase ID token: await user.getIdToken()
   ↓
7. Send to backend with Authorization: Bearer <token>
   ↓
8. Backend verifies Firebase token
   ↓
9. Backend calls Gemini API
   ↓
10. Returns AI response to frontend
```

## 💡 Pro Tips

1. **Keep backend terminal visible** - You'll see errors immediately
2. **Keep browser console open** - Check for frontend errors
3. **Test with simple message first** - "Hello" or "Hi"
4. **Check network tab** - See actual API requests/responses

## 🆘 Still Having Issues?

### Collect this information:

1. **Are you logged in?**
   - Check browser console: `console.log(user)` in DevTools

2. **Backend logs:**
   - Copy any errors from backend terminal

3. **Browser console:**
   - F12 → Console tab → Copy errors

4. **Network request:**
   - F12 → Network tab
   - Find request to `/api/assistant/chat`
   - Check Status, Headers, Response

### Test backend directly:

```bash
# Get your Firebase token first (from browser console):
# await user.getIdToken()

# Then test:
curl -X POST http://127.0.0.2:8000/api/assistant/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -d '{"message": "Hello", "use_rag": false}'
```

## ✨ Success Indicators

You'll know it's working when:
- ✅ No warning banner (when logged in)
- ✅ Message appears in chat
- ✅ Typing indicator shows
- ✅ AI response appears
- ✅ No errors in console or backend logs

---

**Remember:** You MUST be logged in first! The assistant cannot work without authentication.
