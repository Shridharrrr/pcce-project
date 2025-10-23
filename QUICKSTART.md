# Quick Start Guide - WorkSpace Hub

Get your workspace management system up and running in 5 minutes!

## Prerequisites Checklist
- [ ] Node.js 18+ installed
- [ ] Python 3.8+ installed
- [ ] Firebase project created
- [ ] Firestore enabled in Firebase Console

## Step 1: Firebase Setup (5 minutes)

### 1.1 Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Enter project name and follow the wizard

### 1.2 Enable Firestore
1. In Firebase Console, go to "Firestore Database"
2. Click "Create Database"
3. Choose "Start in test mode" (for development)
4. Select a location

### 1.3 Enable Authentication
1. Go to "Authentication" → "Sign-in method"
2. Enable "Email/Password"
3. Enable "Google" (optional but recommended)

### 1.4 Get Service Account Key
1. Go to Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Save the JSON file as `firebase-service-account.json`
4. Move it to the `backend/` directory

### 1.5 Get Web App Config
1. Go to Project Settings → General
2. Scroll to "Your apps" → Click Web icon
3. Register your app
4. Copy the config object

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure firebase-service-account.json is in this directory

# Run the server
python main.py
```

✅ Backend should now be running on `http://127.0.0.1:8000`

## Step 3: Frontend Setup (2 minutes)

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Create .env file
# Copy the template below and fill in your Firebase config
```

### .env Template
```env
NEXT_PUBLIC_FIREBASE_API_KEY=AIza...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
NEXT_PUBLIC_API_URL=http://localhost:8000
```

```bash
# Run the development server
npm run dev
```

✅ Frontend should now be running on `http://localhost:3000`

## Step 4: Test the Application

1. **Open Browser**: Navigate to `http://localhost:3000`
2. **Sign Up**: Click "Get Started" and create an account
3. **Create Project**: Click "New Project" in the dashboard
4. **Add Details**:
   - Name: "My First Project"
   - Description: "Testing the workspace"
   - Members: (optional) add team member emails
5. **Start Chatting**: Select the project and send a message
6. **Verify Firestore**: Check Firebase Console → Firestore to see your data

## Verification Checklist

- [ ] Backend running without errors
- [ ] Frontend loads successfully
- [ ] Can create an account
- [ ] Can log in
- [ ] Dashboard displays
- [ ] Can create a project
- [ ] Can send messages
- [ ] Messages appear in Firestore

## Common Issues & Solutions

### Issue: "Firebase not configured"
**Solution**: Ensure `firebase-service-account.json` is in the `backend/` directory

### Issue: "Module not found" errors
**Solution**: 
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Port already in use"
**Solution**:
```bash
# Find and kill the process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue: Frontend can't connect to backend
**Solution**: 
1. Check backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env`
3. Check CORS is enabled in backend (already configured)

### Issue: Authentication fails
**Solution**:
1. Verify Firebase config in `.env` is correct
2. Check Email/Password is enabled in Firebase Console
3. Clear browser cache and try again

## Next Steps

Once everything is working:

1. **Invite Team Members**: Add real email addresses when creating projects
2. **Customize**: Update branding, colors, and features as needed
3. **Deploy**: Consider deploying to Vercel (frontend) and Railway/Heroku (backend)
4. **Security**: Update Firestore rules for production
5. **Features**: Add file uploads, notifications, video calls, etc.

## Production Deployment

### Firestore Security Rules
Before going to production, update your Firestore rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Team members can read/write team data
    match /teams/{teamId} {
      allow read: if request.auth != null && 
        (resource.data.admin_id == request.auth.uid ||
         request.auth.uid in resource.data.members);
      allow write: if request.auth != null && 
        resource.data.admin_id == request.auth.uid;
    }
    
    // Team members can read/write messages
    match /messages/{messageId} {
      allow read: if request.auth != null;
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null && 
        resource.data.senderId == request.auth.uid;
    }
  }
}
```

## Support

Need help? Check:
- README.md for detailed documentation
- Firebase Console for database issues
- Browser console for frontend errors
- Terminal output for backend errors

Happy collaborating! 🚀
