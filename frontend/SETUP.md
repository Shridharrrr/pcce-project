# Planora Frontend Setup

## Environment Variables

Create a `.env.local` file in the frontend directory with the following variables:

```env
# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=your-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development Mode

The application now includes mock data for development when the backend is not available. This allows you to:

1. **View Projects**: See sample projects in the sidebar
2. **Create Projects**: Add new projects with mock data
3. **Chat Functionality**: Send and receive messages in project chats

## Features

- ✅ **Project Sidebar**: Lists all projects with member avatars
- ✅ **Create Project**: Modal to create new projects with team members
- ✅ **Chat Interface**: Real-time messaging within projects
- ✅ **Mock Data**: Works without backend for development
- ✅ **Error Handling**: Graceful fallbacks when API is unavailable

## Running the Application

1. Install dependencies: `npm install`
2. Set up environment variables (see above)
3. Run development server: `npm run dev`
4. Visit `http://localhost:3000`

The application will automatically use mock data in development mode, so you can test all features without setting up the backend first.
