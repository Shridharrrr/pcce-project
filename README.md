# PCCE Project - Workspace Management Application

A modern workspace management application with real-time chat functionality for different projects. Built with Next.js, FastAPI, and Firebase.

## Features

- 🔐 **Authentication**: Email/password and Google sign-in
- 📁 **Project Management**: Create and manage different projects
- 💬 **Real-time Chat**: Each project has its own chat space
- 👥 **Team Collaboration**: Add team members to projects
- 🔄 **Real-time Updates**: WebSocket support for instant messaging

## Tech Stack

### Frontend
- **Next.js 16** - React framework
- **Tailwind CSS** - Styling
- **Firebase Auth** - Authentication
- **React Context** - State management

### Backend
- **FastAPI** - Python web framework
- **Firebase Admin SDK** - Backend authentication
- **Firestore** - Database
- **WebSockets** - Real-time communication

## Quick Start

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- Firebase project

### 1. Clone the repository
```bash
git clone <repository-url>
cd pcce-project
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Firebase service account key
# Download from Firebase Console > Project Settings > Service Accounts
# Place as: backend/firebase-service-account.json

# Start the backend server
python main.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local with your Firebase configuration
# Get from Firebase Console > Project Settings > General > Your apps

# Start the development server
npm run dev
```

### 4. Firebase Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Authentication:
   - Go to Authentication > Sign-in method
   - Enable Email/Password and Google providers
4. Create Firestore Database:
   - Go to Firestore Database
   - Create database in production mode
5. Get your configuration:
   - Go to Project Settings > General > Your apps
   - Copy the configuration to `.env.local`

### 5. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Usage

1. **Sign Up/Sign In**: Create an account or sign in with Google
2. **Create Projects**: Click "New Project" to create a workspace
3. **Add Team Members**: Invite others by email when creating projects
4. **Start Chatting**: Select a project to access its chat space
5. **Real-time Messaging**: Send messages and see them instantly

## Project Structure

```
pcce-project/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts
│   │   └── config/          # Configuration files
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── dependencies/     # FastAPI dependencies
│   └── main.py
└── README.md
```

## API Endpoints

### Authentication
- `POST /auth/verify` - Verify Firebase token

### Teams/Projects
- `GET /teams/` - Get user's teams
- `POST /teams/` - Create new team
- `GET /teams/{team_id}` - Get specific team
- `PUT /teams/{team_id}` - Update team
- `DELETE /teams/{team_id}` - Delete team

### Messages
- `GET /messages/{team_id}` - Get team messages
- `POST /messages/` - Send message
- `PUT /messages/{message_id}` - Update message
- `DELETE /messages/{message_id}` - Delete message

### WebSocket
- `WS /ws/{team_id}?token={token}` - Real-time chat

## Development

### Running in Development Mode

Use the provided scripts:

**Windows:**
```bash
start-dev.bat
```

**macOS/Linux:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

### Manual Start

**Backend:**
```bash
cd backend
python main.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## Troubleshooting

### Common Issues

1. **Firebase Configuration Error**
   - Ensure `firebase-service-account.json` is in the backend directory
   - Check that all environment variables are set correctly

2. **CORS Errors**
   - Backend is configured to allow all origins in development
   - Check that the frontend is calling the correct API URL

3. **Authentication Issues**
   - Verify Firebase project is properly configured
   - Check that authentication providers are enabled

4. **Database Connection**
   - Ensure Firestore is enabled in your Firebase project
   - Check that the service account has proper permissions

### Debug Mode

Enable debug logging by setting environment variables:
```bash
# Backend
export DEBUG=1
python main.py

# Frontend
export NODE_ENV=development
npm run dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the repository or contact the development team.
