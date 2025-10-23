# PCCE Project Setup Guide

This is a workspace management application with chat functionality for different projects.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- Firebase project

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up Firebase Admin SDK:
   - Download your Firebase service account key from Firebase Console
   - Place it in the backend directory as `firebase-service-account.json`

6. Start the backend server:
   ```bash
   python main.py
   ```

The backend will run on `http://localhost:8000`

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   Create a `.env.local` file in the frontend directory with the following content:
   ```
   NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will run on `http://localhost:3000`

## Firebase Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use an existing one
3. Enable Authentication with Email/Password and Google providers
4. Create a Firestore database
5. Get your Firebase configuration from Project Settings > General > Your apps
6. Update the `.env.local` file with your Firebase configuration

## Features

- **Authentication**: Email/password and Google sign-in
- **Project Management**: Create and manage different projects
- **Chat System**: Each project has its own chat space
- **Real-time Messaging**: WebSocket support for real-time chat
- **User Management**: Add team members to projects

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Sign up or sign in with your credentials
4. Create a new project
5. Start chatting with your team members

## Troubleshooting

- Make sure both servers are running
- Check that Firebase configuration is correct
- Ensure all environment variables are set
- Check browser console for any errors
