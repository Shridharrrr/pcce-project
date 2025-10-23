"use client";

import { useAuth } from "../../contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import ProjectSidebar from "../../components/ProjectSidebar";
import ChatInterface from "../../components/ChatInterface";
import AddProjectModal from "../../components/AddProjectModal";
import ProtectedRoute from "../../components/ProtectedRoute";

export default function Dashboard() {
  const { user, logout, getIdToken } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showAddProjectModal, setShowAddProjectModal] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

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
      <div className="h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">WorkSpace Hub</h1>
              <nav className="ml-8 flex space-x-4">
                <Link
                  href="/dashboard"
                  className="text-blue-600 font-medium border-b-2 border-blue-600 px-3 py-2"
                >
                  Dashboard
                </Link>
                <Link
                  href="/profile"
                  className="text-gray-500 hover:text-gray-700 px-3 py-2"
                >
                  Profile
                </Link>
              </nav>
            </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3">
                  {userData?.photoURL ? (
                    <img
                      src={userData.photoURL}
                      alt="Profile"
                      className="h-8 w-8 rounded-full"
                    />
                  ) : (
                    <div className="h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">
                        {userData?.name?.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                  <span className="text-sm font-medium text-gray-700">
                    {userData?.name}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex h-screen">
          {/* Project Sidebar */}
          <ProjectSidebar
            selectedProject={selectedProject}
            onProjectSelect={handleProjectSelect}
            onCreateProject={handleCreateProject}
            refreshTrigger={refreshTrigger}
          />
          
          {/* Chat Interface */}
          <ChatInterface selectedProject={selectedProject} />
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
