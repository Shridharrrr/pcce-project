# WorkSpace Hub - Team Collaboration Platform

A modern workspace management system that enables teams to collaborate efficiently through real-time chat, project management, and seamless team coordination. All conversations are automatically saved to Firebase Firestore.

## Features

### 🏠 Landing Page
- Clean, modern landing page introducing the workspace management system
- Automatic redirect to dashboard for authenticated users
- Call-to-action buttons for getting started

### 🔐 Authentication
- Email/Password authentication via Firebase
- Google Sign-In integration
- Secure token-based authentication
- Protected routes for authenticated users only

### 📊 Dashboard
- **Project Management**: Create and manage multiple projects
- **Team Collaboration**: Add members to projects via email
- **Real-time Chat**: Each project has its own dedicated chat room
- **Project Sidebar**: Quick access to all your projects
- **User Profile**: Display user information and avatar

### 💬 Chat Features
- Real-time messaging within each project
- Message history automatically saved to Firestore
- Sender identification with avatars
- Timestamp for each message
- Responsive chat interface

### 👥 Team Management
- Create projects with name and description
- Add multiple team members via email addresses
- View all project members
- Admin controls for project management

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Firebase Admin SDK**: Authentication and Firestore integration
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 16**: React framework with App Router
- **React 19**: Latest React features
- **Firebase SDK**: Client-side authentication
- **Tailwind CSS 4**: Utility-first styling
- **Geist Font**: Modern typography

### Database
- **Firebase Firestore**: NoSQL cloud database for real-time data sync

## Project Structure

```
pcce-project/
├── backend/
│   ├── app/
│   │   ├── dependencies/
│   │   │   └── auth.py          # Authentication middleware
│   │   ├── models/
│   │   │   ├── message.py       # Message data models
│   │   │   ├── teams.py         # Team data models
│   │   │   └── users.py         # User data models
│   │   ├── routes/
│   │   │   ├── auth.py          # Auth endpoints
│   │   │   ├── message_routes.py # Message CRUD
│   │   │   ├── team_routes.py   # Team management
│   │   │   └── user_routes.py   # User management
│   │   └── services/
│   │       ├── firestore_service.py  # Firestore operations
│   │       └── websocket_service.py  # WebSocket support
│   ├── config.py                # Firebase configuration
│   ├── main.py                  # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── firebase-service-account.json  # Firebase credentials
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/
│   │   │   │   └── page.js      # Authentication page
│   │   │   ├── dashboard/
│   │   │   │   └── page.js      # Main dashboard
│   │   │   ├── layout.js        # Root layout
│   │   │   ├── page.js          # Landing page
│   │   │   └── globals.css      # Global styles
│   │   ├── components/
│   │   │   ├── AddProjectModal.jsx   # Create project modal
│   │   │   ├── ChatInterface.jsx     # Chat UI
│   │   │   ├── ProjectSidebar.jsx    # Project list
│   │   │   └── ProtectedRoute.jsx    # Auth guard
│   │   ├── config/
│   │   │   └── firebase.js      # Firebase client config
│   │   └── contexts/
│   │       └── AuthContext.js   # Auth state management
│   ├── package.json
│   └── .env                     # Environment variables
│
└── README.md
```

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Firebase project with Firestore enabled

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Firebase:**
   - Download your Firebase service account JSON from Firebase Console
   - Save it as `firebase-service-account.json` in the backend directory

6. **Run the backend:**
   ```bash
   python main.py
   ```
   Backend will run on `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   Create a `.env` file with your Firebase configuration:
   ```env
   NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
   NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/verify-token` - Verify Firebase ID token
- `GET /auth/me` - Get current user info

### Teams/Projects
- `POST /teams/` - Create new project
- `GET /teams/` - Get user's projects
- `GET /teams/{team_id}` - Get specific project
- `PUT /teams/{team_id}` - Update project
- `DELETE /teams/{team_id}` - Delete project
- `POST /teams/{team_id}/members` - Add member
- `DELETE /teams/{team_id}/members/{member_id}` - Remove member

### Messages
- `POST /messages/` - Send message
- `GET /messages/{team_id}` - Get project messages
- `PUT /messages/{message_id}` - Update message
- `DELETE /messages/{message_id}` - Delete message

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `GET /me/teams` - Get user's teams

## Usage Flow

1. **Landing Page** → User visits the homepage
2. **Authentication** → User signs up or logs in
3. **Dashboard** → Redirected to dashboard after authentication
4. **Create Project** → Click "New Project" to create a workspace
5. **Add Members** → Enter email addresses of team members
6. **Start Chatting** → Select project and start collaborating
7. **Real-time Sync** → All messages automatically saved to Firestore

## Features in Detail

### Project Creation
- **Name**: Required field for project identification
- **Description**: Optional field to describe the project
- **Members**: Add team members by entering comma-separated email addresses
- Each project automatically creates a dedicated chat room

### Chat System
- Messages are linked to specific projects (teamId)
- Each message includes:
  - Sender information (name, email, avatar)
  - Message content
  - Timestamp
  - Message type (text, file, etc.)
- Messages are stored in Firestore `messages` collection
- Real-time updates via Firebase listeners

### Data Storage in Firestore

**Collections:**
- `users` - User profiles and team memberships
- `teams` - Project information and members
- `messages` - Chat messages linked to teams
- `team_invites` - Pending team invitations

**Message Document Structure:**
```json
{
  "messageId": "unique-id",
  "teamId": "project-id",
  "senderId": "user-id",
  "sender_email": "user@example.com",
  "sender_name": "User Name",
  "content": "Message text",
  "message_type": "text",
  "created_at": "2024-01-01T00:00:00Z",
  "status": "sent"
}
```

## Security

- Firebase Authentication for secure user management
- JWT token validation on all protected endpoints
- Role-based access control (admin/member)
- CORS configured for frontend-backend communication
- Protected routes on frontend using AuthContext

## Development

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build
npm start
```

## Troubleshooting

### Backend Issues
- **Firebase not configured**: Ensure `firebase-service-account.json` is in the backend directory
- **Port already in use**: Change port in `main.py` or kill the process using port 8000

### Frontend Issues
- **Firebase config error**: Check `.env` file has all required variables
- **API connection failed**: Ensure backend is running on correct port
- **Build errors**: Delete `.next` folder and `node_modules`, then reinstall

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.
