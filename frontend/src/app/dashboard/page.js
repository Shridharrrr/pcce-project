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
import {
  Instrument_Serif,
  Domine,
  Electrolize,
  Rajdhani,
} from "next/font/google";

const domine = Domine({
  subsets: ["latin"],
  weight: "600",
});

const instrumentSerif = Instrument_Serif({
  subsets: ["latin"],
  weight: "400",
  display: "swap",
});

const electrolize = Electrolize({
  subsets: ["latin"],
  weight: "400",
});

const rajdhani = Rajdhani({
  subsets: ["latin"],
  weight: "700",
});

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
    setRefreshTrigger((prev) => prev + 1);
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
      <div className="h-screen bg-white flex flex-col">
        {/* Header */}
        <header className="bg-white  border-b border-gray-200">
          <div className="px-4 sm:px-6 lg:px-6">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className={`text-2xl font-extrabold tracking-wider ${rajdhani.className}`} style={{ color: '#2563eb' }}>
                  SYNAPSE
                </h1>
              </div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3 px-3 py-2 ">
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
                  className="bg-white text-red-500 px-4 py-2 rounded-lg text-base font-medium transition-all hover:text-red-700"
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
            onProjectsLoaded={setProjects}
          />

          {/* Main Content Area */}
          {showThinkBuddy ? (
            <ThinkBuddyAssistant
              projects={Array.isArray(projects) ? projects : []}
            />
          ) : (
            <div className="flex-1 flex flex-col overflow-hidden">
              {/* Tab Navigation */}
              {selectedProject && (
                <div className="bg-white border-b border-gray-200 px-4">
                  <div className="flex gap-4">
                    <button
                      onClick={() => setActiveTab("chat")}
                      className={`px-4 py-3 font-medium transition-colors border-b-2 ${
                        activeTab === "chat"
                          ? "text-blue-600 border-blue-600"
                          : "text-gray-500 border-transparent hover:text-gray-700"
                      }`}
                    >
                      Chat
                    </button>
                    <button
                      onClick={() => setActiveTab("todos")}
                      className={`px-4 py-3 font-medium transition-colors border-b-2 ${
                        activeTab === "todos"
                          ? "text-blue-600 border-blue-600"
                          : "text-gray-500 border-transparent hover:text-gray-700"
                      }`}
                    >
                      Todos
                    </button>
                    <button
                      onClick={() => setActiveTab("summary")}
                      className={`px-4 py-3 font-medium transition-colors border-b-2 ${
                        activeTab === "summary"
                          ? "text-blue-600 border-blue-600"
                          : "text-gray-500 border-transparent hover:text-gray-700"
                      }`}
                    >
                      Summary
                    </button>
                  </div>
                </div>
              )}

              {/* Content based on active tab */}
              <div className="flex-1 overflow-hidden">
                {activeTab === "chat" ? (
                  <ChatInterface selectedProject={selectedProject} />
                ) : activeTab === "todos" ? (
                  <TodoList selectedProject={selectedProject} />
                ) : (
                  <ChatSummary selectedProject={selectedProject} />
                )}
              </div>
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
