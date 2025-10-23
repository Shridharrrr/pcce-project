# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Start the Frontend (Works without backend!)
```bash
cd frontend
npm install
npm run dev
```

The app will run on http://localhost:3000

### 2. Test the Demo Mode
- The app now works in **Demo Mode** without requiring backend setup
- You'll see sample projects and can create new ones
- Chat functionality works with mock data
- Look for the "Demo Mode" indicator in the header

### 3. Optional: Start the Backend (for full functionality)
```bash
cd backend
pip install -r requirements.txt
python main.py
```

## 🎯 What You Can Do in Demo Mode

### ✅ **Working Features:**
- **Authentication**: Sign up/sign in (Firebase required)
- **Project Management**: Create, view, and manage projects
- **Chat System**: Send and receive messages in each project
- **Team Collaboration**: Add team members to projects
- **Real-time UI**: Responsive interface with loading states

### 📱 **User Experience:**
1. **Sign Up/In**: Create account or use Google sign-in
2. **Dashboard**: See your projects and create new ones
3. **Project Chat**: Click on any project to start chatting
4. **Create Projects**: Use the "New Project" button to add workspaces
5. **Team Management**: Add members when creating projects

## 🔧 Demo Mode Features

### **Sample Projects:**
- **Sample Project**: Basic project with welcome messages
- **Development Team**: Team collaboration example
- **Custom Projects**: Create your own projects

### **Mock Data:**
- Pre-loaded sample messages
- Team member avatars
- Project descriptions
- Timestamps and user info

## 🚨 Troubleshooting

### **If you see a spinner:**
- The app is trying to connect to the backend
- Wait a few seconds - it will switch to demo mode
- Look for the "Demo Mode" indicator

### **If authentication fails:**
- Check that Firebase is configured
- See `CONFIGURATION.md` for setup instructions
- The app will show appropriate error messages

### **If the sidebar is empty:**
- This is normal in demo mode
- Click "New Project" to create your first project
- The sidebar will populate with your projects

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Loading States**: Smooth transitions and feedback
- **Error Handling**: Clear error messages and recovery options
- **Keyboard Shortcuts**: Press Enter to send messages
- **Real-time Updates**: Instant UI updates

## 🔄 Next Steps

1. **Try the Demo**: Explore all features in demo mode
2. **Set up Backend**: Follow `CONFIGURATION.md` for full functionality
3. **Customize**: Modify the UI and add your own features
4. **Deploy**: Use the provided scripts to deploy to production

## 📞 Support

- Check the console for any error messages
- Look for the "Demo Mode" indicator to confirm offline mode
- All features work without backend - perfect for development and testing!

---

**🎉 You're ready to go! The app now works completely in demo mode without any backend setup required.**
