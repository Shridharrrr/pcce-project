# Configuration Guide

## Frontend Environment Variables

Create a `.env.local` file in the `frontend` directory with the following content:

```env
# Firebase Configuration
# Get these values from Firebase Console > Project Settings > General > Your apps
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key_here
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Backend Configuration

1. **Firebase Service Account**
   - Go to Firebase Console > Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file
   - Rename it to `firebase-service-account.json`
   - Place it in the `backend` directory

2. **Firebase Project Setup**
   - Enable Authentication with Email/Password and Google providers
   - Create a Firestore database
   - Set up security rules (for development, you can use test mode)

## Firebase Security Rules (Development)

For development, you can use these permissive rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Production Configuration

For production, implement proper security rules and environment variables:

1. Use environment variables for all sensitive data
2. Implement proper Firestore security rules
3. Enable CORS restrictions
4. Use HTTPS for all communications
5. Implement rate limiting
6. Add proper error handling and logging

## Troubleshooting

### Common Issues

1. **"Firebase not configured" error**
   - Check that all environment variables are set
   - Verify Firebase project is properly configured
   - Ensure service account file is in the correct location

2. **CORS errors**
   - Backend is configured to allow all origins in development
   - For production, update CORS settings in `backend/main.py`

3. **Authentication not working**
   - Verify Firebase Auth is enabled
   - Check that providers (Email/Password, Google) are enabled
   - Ensure environment variables match your Firebase project

4. **Database connection issues**
   - Verify Firestore is enabled
   - Check service account permissions
   - Ensure database rules allow access

### Testing Configuration

Run the test script to verify backend configuration:

```bash
python test-backend.py
```

This will test:
- Backend connectivity
- API endpoints
- Authentication requirements
- Documentation accessibility
