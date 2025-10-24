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
import TodoList from "../../components/TodoList";
import ChatSummary from "../../components/ChatSummary";

export default function Dashboard() {
  const { user, logout, getIdToken } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showAddProjectModal, setShowAddProjectModal] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [showThinkBuddy, setShowThinkBuddy] = useState(false);
  const [projects, setProjects] = useState([]);
  const [activeTab, setActiveTab] = useState("chat"); // "chat" or "todos"

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
      <div className="h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col overflow-hidden">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 flex-shrink-0">
        <div className="px-6 lg:px-8">
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
              <nav className="ml-10 flex space-x-1">
                <Link
                  href="/dashboard"
                  className="text-blue-600 font-semibold bg-blue-50 border-b-2 border-blue-600 px-5 py-2 rounded-t-lg transition-all"
                >
                  Dashboard
                </Link>
              </nav>
            </div>

              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-3 bg-gray-50 px-4 py-2 rounded-lg border border-gray-200">
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
                  className="bg-gradient-to-r from-red-50 to-red-100 hover:from-red-100 hover:to-red-200 text-red-600 px-5 py-2 rounded-lg text-sm font-medium transition-all shadow-sm hover:shadow-md border border-red-200"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex overflow-hidden">
          {/* Project Sidebar */}
          <ProjectSidebar
            selectedProject={selectedProject}
            onProjectSelect={handleProjectSelect}
            onCreateProject={handleCreateProject}
            refreshTrigger={refreshTrigger}
            onThinkBuddyClick={handleThinkBuddyClick}
            onProjectsLoaded={setProjects}
          />
          
          {/* Main Content Area */}
          {showThinkBuddy ? (
            <ThinkBuddyAssistant projects={Array.isArray(projects) ? projects : []} />

          ) : (
            <div className="flex-1 flex flex-col">
              {/* Tab Navigation */}
              {selectedProject && (
                <div className="bg-white border-b border-gray-200 px-6 shadow-sm">
                  <div className="flex gap-6">
                    <button
                      onClick={() => setActiveTab("chat")}
                      className={`px-1 py-3 font-semibold transition-all border-b-2 ${
                        activeTab === "chat"
                          ? "text-blue-600 border-blue-600"
                          : "text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300"
                      }`}
                    >
                      💬 Chat
                    </button>
                    <button
                      onClick={() => setActiveTab("todos")}
                      className={`px-1 py-3 font-semibold transition-all border-b-2 ${
                        activeTab === "todos"
                          ? "text-blue-600 border-blue-600"
                          : "text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300"
                      }`}
                    >
                      ✓ Todos
                    </button>
                    <button
                      onClick={() => setActiveTab("summary")}
                      className={`px-1 py-3 font-semibold transition-all border-b-2 ${
                        activeTab === "summary"
                          ? "text-blue-600 border-blue-600"
                          : "text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300"
                      }`}
                    >
                      📊 Summary
                    </button>
                  </div>
                </div>
              )}
              
              {/* Content based on active tab */}
              {activeTab === "chat" ? (
                <ChatInterface selectedProject={selectedProject} />
              ) : activeTab === "todos" ? (
                <TodoList selectedProject={selectedProject} />
              ) : (
                <ChatSummary selectedProject={selectedProject} />
              )}
            </div>
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
