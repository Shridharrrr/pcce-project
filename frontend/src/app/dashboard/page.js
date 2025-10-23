"use client";

import { useAuth } from "../../contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import ProjectSidebar from "../../components/ProjectSidebar";
import ChatInterface from "../../components/ChatInterface";
import AddProjectModal from "../../components/AddProjectModal";
import ProtectedRoute from "../../components/ProtectedRoute";
import ThinkBuddyAssistant from "../../components/ThinkBuddyAssistant";

export default function Dashboard() {
  const { user, logout, getIdToken } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showAddProjectModal, setShowAddProjectModal] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [showThinkBuddy, setShowThinkBuddy] = useState(false);

  useEffect(() => {
    if (!user) {
      router.push("/auth");
      return;
    }

    // Simulate fetching user data
    const fetchUserData = async () => {
      try {
        const token = await getIdToken();
        console.log(token);
        setUserData({
          name: user.displayName || user.email.split("@")[0],
          email: user.email,
          joinDate: new Date(user.metadata.creationTime).toLocaleDateString(),
          isEmailVerified: user.emailVerified,
          photoURL: user.photoURL,
        });
      } catch (error) {
        console.error("Error fetching user data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [user, router, getIdToken]);

  const handleLogout = async () => {
    try {
      await logout();
      router.push("/");
    } catch (error) {
      console.error("Failed to logout:", error);
    }
  };

  const handleProjectSelect = (project) => {
    setSelectedProject(project);
    setShowThinkBuddy(false);
  };

  const handleThinkBuddyClick = () => {
    setShowThinkBuddy(true);
    setSelectedProject(null);
  };

  const handleCreateProject = () => {
    setShowAddProjectModal(true);
  };

  const handleProjectCreated = (newProject) => {
    setSelectedProject(newProject);
    setRefreshTrigger(prev => prev + 1);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-md">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">WorkSpace Hub</h1>
              </div>
              <nav className="ml-8 flex space-x-2">
                <Link
                  href="/dashboard"
                  className="text-blue-600 font-semibold bg-blue-50 border-b-2 border-blue-600 px-4 py-2 rounded-t-lg transition-all"
                >
                  Dashboard
                </Link>
                <Link
                  href="/profile"
                  className="text-gray-500 hover:text-gray-700 hover:bg-gray-50 px-4 py-2 rounded-t-lg transition-all"
                >
                  Profile
                </Link>
              </nav>
            </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3 bg-gray-50 px-3 py-2 rounded-lg">
                  {userData?.photoURL ? (
                    <img
                      src={userData.photoURL}
                      alt="Profile"
                      className="h-8 w-8 rounded-full shadow-sm"
                    />
                  ) : (
                    <div className="h-8 w-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-sm">
                      <span className="text-white text-sm font-medium">
                        {userData?.name?.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                  <span className="text-sm font-semibold text-gray-700">
                    {userData?.name}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-all shadow-sm hover:shadow-md"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex h-screen overflow-hidden">
          {/* Project Sidebar */}
          <ProjectSidebar
            selectedProject={selectedProject}
            onProjectSelect={handleProjectSelect}
            onCreateProject={handleCreateProject}
            refreshTrigger={refreshTrigger}
            onThinkBuddyClick={handleThinkBuddyClick}
          />
          
          {/* Main Content Area */}
          {showThinkBuddy ? (
            <ThinkBuddyAssistant />
          ) : (
            <ChatInterface selectedProject={selectedProject} />
          )}
        </main>

        {/* Add Project Modal */}
        <AddProjectModal
          isOpen={showAddProjectModal}
          onClose={() => setShowAddProjectModal(false)}
          onProjectCreated={handleProjectCreated}
        />
      </div>
    </ProtectedRoute>
  );
}
