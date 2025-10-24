"use client";

import { useState, useEffect, useRef } from "react";
import { useAuth } from "../contexts/AuthContext";

const PREDEFINED_PROMPTS = [
  "Explain this code snippet",
  "Help me debug an issue",
  "Suggest best practices",
  "Generate project ideas",
  "Review my code",
];

const ThinkBuddyAssistant = ({ projects = [] }) => {
  const { user, getIdToken } = useAuth();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [selectedProject, setSelectedProject] = useState("general");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const availableProjects = projects.length > 0 ? [
    { teamId: "general", teamName: "General", description: "General questions and assistance" },
    ...projects
  ] : [
    { teamId: "general", teamName: "General", description: "General questions and assistance" },
    { teamId: "webdev", teamName: "Web Development", description: "Frontend, backend, and full-stack" },
    { teamId: "ai", teamName: "AI & Machine Learning", description: "AI models, training, and deployment" },
    { teamId: "mobile", teamName: "Mobile Development", description: "iOS, Android, and cross-platform" },
  ];

  // Load chat history for the selected project
  const loadChatHistory = async (projectContext) => {
    if (!user) {
      setIsLoadingHistory(false);
      return;
    }

    setIsLoadingHistory(true);

    try {
      const token = await getIdToken();
      if (!token) {
        setIsLoadingHistory(false);
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/assistant/history?project_context=${projectContext}`,
        {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        if (data.history && data.history.length > 0) {
          // Transform the history to match the message format
          const transformedMessages = data.history.map((msg, index) => ({
            id: index + 1,
            role: msg.role,
            content: msg.content,
            timestamp: msg.timestamp,
            sources: msg.sources || [],
            project_context: msg.project_context || "general"
          }));
          setMessages(transformedMessages);
        } else {
          // No history, show welcome message
          setMessages([{
            id: 1,
            role: "assistant",
            content: "Hello! I'm ThinkBuddy, your AI assistant. Select a project context and ask me anything!",
            timestamp: new Date().toISOString()
          }]);
        }
      } else {
        // Failed to load, show welcome message
        setMessages([{
          id: 1,
          role: "assistant",
          content: "Hello! I'm ThinkBuddy, your AI assistant. Select a project context and ask me anything!",
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
      // Show welcome message on error
      setMessages([{
        id: 1,
        role: "assistant",
        content: "Hello! I'm ThinkBuddy, your AI assistant. Select a project context and ask me anything!",
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  // Load chat history on mount
  useEffect(() => {
    loadChatHistory(selectedProject);
  }, [user, getIdToken]);

  // Load chat history when project changes
  useEffect(() => {
    if (user) {
      loadChatHistory(selectedProject);
    }
  }, [selectedProject]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendMessage = async (customMessage) => {
    // Check if customMessage is an event object and ignore it
    const messageToSend = (typeof customMessage === 'string' ? customMessage : inputMessage).trim();
    if (!messageToSend || isTyping) return;

    const userMessage = {
      id: messages.length + 1,
      role: "user",
      content: messageToSend,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsTyping(true);

    try {
      // Get authentication token
      const token = await getIdToken();
      
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Call the real AI assistant API
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/assistant/chat`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: messageToSend,
            project_context: selectedProject !== 'general' ? selectedProject : null,
            use_rag: true
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      
      const assistantMessage = {
        id: messages.length + 2,
        role: "assistant",
        content: data.response,
        timestamp: data.timestamp || new Date().toISOString(),
        sources: data.sources || []
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error calling AI assistant:', error);
      
      // Fallback to mock response if API fails
      const aiResponse = generateAIResponse(messageToSend);
      const assistantMessage = {
        id: messages.length + 2,
        role: "assistant",
        content: `⚠️ Using offline mode. ${aiResponse}`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handlePredefinedPrompt = (prompt) => {
    handleSendMessage(prompt);
  };

  // Mock AI response generator (replace with actual API integration)
  const generateAIResponse = (userInput) => {
    const projectContext = availableProjects.find(p => p.teamId === selectedProject);
    const contextName = projectContext?.teamName || "General";
    
    return `Based on your "${contextName}" project context: I understand you're asking about "${userInput}". This is a simulated response. In a real implementation, this would connect to an AI API to provide intelligent responses based on your project context.`;
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleClearChat = async () => {
    const projectName = availableProjects.find(p => p.teamId === selectedProject)?.teamName || "General";
    if (!confirm(`Are you sure you want to clear your chat history for "${projectName}"? This cannot be undone.`)) {
      return;
    }

    try {
      const token = await getIdToken();
      if (!token) {
        throw new Error('No authentication token available');
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/assistant/clear-history?project_context=${selectedProject}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.ok) {
        // Clear local messages and show welcome message
        setMessages([{
          id: 1,
          role: "assistant",
          content: "Hello! I'm ThinkBuddy, your AI assistant. Select a project context and ask me anything!",
          timestamp: new Date().toISOString()
        }]);
      } else {
        console.error('Failed to clear chat history');
        alert('Failed to clear chat history. Please try again.');
      }
    } catch (error) {
      console.error('Error clearing chat history:', error);
      alert('Error clearing chat history. Please try again.');
    }
  };


  return (
    <div className="flex-1 bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col h-full">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-md">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900">
                ThinkBuddy - {availableProjects.find(p => p.teamId === selectedProject)?.teamName || "General"}
              </h2>
              <p className="text-xs text-gray-500">Your AI-powered productivity companion</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleClearChat}
              className="px-3 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-2"
              title="Clear chat history"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Clear
            </button>
            <span className="text-sm font-medium text-gray-700">Project:</span>
            <select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none bg-white text-sm shadow-sm text-gray-900 font-medium hover:border-purple-400 transition-colors"
            >
              {availableProjects.map((project) => (
                <option key={project.teamId} value={project.teamId}>
                  {project.teamName}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {isLoadingHistory ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading your chat history...</p>
            </div>
          </div>
        ) : (
          <>
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex gap-3 max-w-3xl ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              {/* Avatar */}
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.role === 'user' 
                  ? 'bg-gradient-to-br from-blue-500 to-blue-600' 
                  : 'bg-gradient-to-br from-purple-500 to-indigo-600'
              } shadow-md`}>
                {message.role === 'user' ? (
                  <span className="text-white text-sm font-medium">
                    {user?.displayName?.charAt(0).toUpperCase() || user?.email?.charAt(0).toUpperCase() || 'U'}
                  </span>
                ) : (
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                )}
              </div>

              {/* Message Content */}
              <div className={`flex flex-col ${message.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`px-4 py-3 rounded-2xl shadow-sm ${
                  message.role === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                    : 'bg-white text-gray-900 border border-gray-200'
                }`}>
                  <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
                  
                  {/* Show sources if available */}
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-xs font-semibold text-gray-500 mb-2">📚 Sources from project context:</p>
                      <div className="space-y-1">
                        {message.sources.map((source, idx) => (
                          <div key={idx} className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                            <span className="font-medium">{source.sender}:</span> {source.content}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
                <span className="text-xs text-gray-400 mt-1 px-1">
                  {formatTime(message.timestamp)}
                </span>
              </div>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="flex gap-3 max-w-3xl">
              <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-gradient-to-br from-purple-500 to-indigo-600 shadow-md">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl shadow-sm">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4 shadow-lg">
        <div className="max-w-4xl mx-auto space-y-4">
          {/* Predefined Prompts */}
          <div className="flex flex-wrap gap-2">
            {PREDEFINED_PROMPTS.map((prompt, index) => (
              <button
                key={index}
                onClick={() => handlePredefinedPrompt(prompt)}
                disabled={isTyping}
                className="bg-gradient-to-r from-purple-50 to-indigo-50 hover:from-purple-100 hover:to-indigo-100 text-purple-700 px-4 py-2 rounded-full text-sm font-medium transition-all shadow-sm hover:shadow-md flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed border border-purple-200"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                {prompt}
              </button>
            ))}
          </div>

          {/* Input Field */}
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything... (Press Enter to send, Shift+Enter for new line)"
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none resize-none shadow-sm text-gray-900 placeholder:text-gray-400"
                rows="1"
                style={{ minHeight: '48px', maxHeight: '120px' }}
                disabled={isTyping}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping}
              className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-300 disabled:to-gray-400 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-md hover:shadow-lg flex items-center gap-2 disabled:cursor-not-allowed"
            >
              {isTyping ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                  Send
                </>
              )}
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2 text-center">
            ThinkBuddy can make mistakes. Consider checking important information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ThinkBuddyAssistant;
