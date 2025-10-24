"use client";

import { useState, useEffect, useRef } from "react";
import { useAuth } from "../contexts/AuthContext";

const ChatInterface = ({ selectedProject }) => {
  const { getIdToken, user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (selectedProject) {
      fetchMessages(true); // Initial load with spinner
      
      // Set up auto-refresh every 3 seconds (without spinner)
      const intervalId = setInterval(() => {
        fetchMessages(false);
      }, 3000);
      
      // Cleanup interval on unmount or when project changes
      return () => clearInterval(intervalId);
    } else {
      setMessages([]);
    }
  }, [selectedProject]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle Enter key to send message
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchMessages = async (showLoader = true) => {
    if (!selectedProject) return;

    try {
      // Only show loading spinner on initial load
      if (showLoader) {
        setLoading(true);
      }
      setError(null);
      
      const token = await getIdToken();
      
      if (!token) {
        throw new Error('No authentication token available');
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/messages/${selectedProject.teamId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', response.status, errorText);
        
        // Handle specific error cases
        if (response.status === 401) {
          throw new Error('Authentication failed. Please login again.');
        } else if (response.status === 500) {
          throw new Error('Server error. Please try again later.');
        } else if (response.status === 404) {
          // No messages found, return empty array
          setMessages([]);
          return;
        } else {
          throw new Error(`Failed to fetch messages: ${response.status}`);
        }
      }

      const data = await response.json();
      setMessages(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching messages:', err);
      // Only show error on initial load, not on auto-refresh
      if (showLoader) {
        setError(err.message || 'Failed to load messages');
      }
      
      // For demo mode, show mock messages
      if (selectedProject.teamId.startsWith('mock-')) {
        setMessages(getMockMessages(selectedProject.teamId));
        setError(null);
      } else if (showLoader) {
        setMessages([]);
      }
    } finally {
      if (showLoader) {
        setLoading(false);
      }
    }
  };

  // Mock messages for demo mode
  const getMockMessages = (teamId) => {
    const mockMessages = {
      'mock-1': [
        {
          messageId: 'msg-1',
          teamId: teamId,
          senderId: user?.uid || 'mock-user',
          sender_email: user?.email || 'user@example.com',
          sender_name: user?.displayName || 'User',
          content: 'Welcome to the Sample Project! This is a demo message.',
          message_type: 'text',
          created_at: new Date(Date.now() - 3600000).toISOString()
        },
        {
          messageId: 'msg-2',
          teamId: teamId,
          senderId: 'mock-user-2',
          sender_email: 'teammate@example.com',
          sender_name: 'Teammate',
          content: 'Thanks for setting this up! Looking forward to working together.',
          message_type: 'text',
          created_at: new Date(Date.now() - 1800000).toISOString()
        }
      ],
      'mock-2': [
        {
          messageId: 'msg-3',
          teamId: teamId,
          senderId: user?.uid || 'mock-user',
          sender_email: user?.email || 'user@example.com',
          sender_name: user?.displayName || 'User',
          content: 'Let\'s discuss the new features we need to implement.',
          message_type: 'text',
          created_at: new Date(Date.now() - 7200000).toISOString()
        },
        {
          messageId: 'msg-4',
          teamId: teamId,
          senderId: 'mock-dev-1',
          sender_email: 'dev1@example.com',
          sender_name: 'Developer 1',
          content: 'I\'ve started working on the authentication module. Should be ready by tomorrow.',
          message_type: 'text',
          created_at: new Date(Date.now() - 3600000).toISOString()
        },
        {
          messageId: 'msg-5',
          teamId: teamId,
          senderId: user?.uid || 'mock-user',
          sender_email: user?.email || 'user@example.com',
          sender_name: user?.displayName || 'User',
          content: 'Great! Keep me updated on the progress.',
          message_type: 'text',
          created_at: new Date(Date.now() - 1800000).toISOString()
        }
      ]
    };
    
    return mockMessages[teamId] || [];
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedProject || sending) return;

    const messageText = newMessage.trim();
    setNewMessage(""); // Clear input immediately for better UX

    // Handle demo mode
    if (selectedProject.teamId.startsWith('mock-')) {
      const newMessageObj = {
        messageId: `msg-${Date.now()}`,
        teamId: selectedProject.teamId,
        senderId: user?.uid || 'mock-user',
        sender_email: user?.email || 'user@example.com',
        sender_name: user?.displayName || 'User',
        content: messageText,
        message_type: 'text',
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, newMessageObj]);
      return;
    }

    try {
      setSending(true);
      setError(null);
      
      const token = await getIdToken();
      
      if (!token) {
        throw new Error('No authentication token available');
      }
      
      const messageData = {
        team_id: selectedProject.teamId,
        content: messageText,
        message_type: "text",
        metadata: {}
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/messages/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(messageData),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', response.status, errorText);
        throw new Error(`Failed to send message: ${response.status}`);
      }

      const sentMessage = await response.json();
      setMessages(prev => [...prev, sentMessage]);
      
      // Refresh messages immediately after sending to get any updates
      setTimeout(() => fetchMessages(false), 500);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message');
      // Restore message on error
      setNewMessage(messageText);
    } finally {
      setSending(false);
    }
  };

  const formatTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  };

  const isMyMessage = (message) => {
    return message.senderId === user?.uid;
  };

  if (!selectedProject) {
    return (
      <div className="flex-1 bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center mt-60">
        <div className="text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <svg className="w-10 h-10 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">Select a Project</h3>
          <p className="text-gray-500">Choose a project from the sidebar to start chatting</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gradient-to-br from-white to-gray-50 flex flex-col overflow-hidden">
      {/* Chat Header */}
      <div className="border-b border-gray-200 p-4 bg-white shadow-sm flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-md">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-900">{selectedProject.teamName}</h2>
              <p className="text-xs text-gray-500">
                {selectedProject.members?.length} member{selectedProject.members?.length !== 1 ? 's' : ''}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex -space-x-2">
              {selectedProject.members?.slice(0, 4).map((member, index) => (
                <div
                  key={index}
                  className="w-9 h-9 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center border-2 border-white shadow-md"
                >
                  <span className="text-white text-sm font-medium">
                    {member.name?.charAt(0).toUpperCase() || member.email?.charAt(0).toUpperCase()}
                  </span>
                </div>
              ))}
              {selectedProject.members?.length > 4 && (
                <div className="w-9 h-9 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full flex items-center justify-center border-2 border-white shadow-md">
                  <span className="text-gray-600 text-sm font-medium">
                    +{selectedProject.members.length - 4}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p className="text-red-600 mb-2">{error}</p>
              <button
                onClick={fetchMessages}
                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                Try again
              </button>
            </div>
          </div>
        ) : messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No messages yet</h3>
              <p className="text-gray-500">Start the conversation by sending a message</p>
            </div>
          </div>
        ) : (
          messages.map((message, index) => {
            const showDate = index === 0 || 
              formatDate(messages[index - 1].created_at) !== formatDate(message.created_at);
            
            return (
              <div key={message.messageId}>
                {showDate && (
                  <div className="flex items-center justify-center my-4">
                    <div className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm">
                      {formatDate(message.created_at)}
                    </div>
                  </div>
                )}
                
                <div className={`flex ${isMyMessage(message) ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-sm ${
                    isMyMessage(message)
                      ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                      : 'bg-white text-gray-900 border border-gray-200'
                  }`}>
                    <div className="flex items-start space-x-2">
                      {!isMyMessage(message) && (
                        <div className="w-6 h-6 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm">
                          <span className="text-white text-xs font-medium">
                            {message.sender_name?.charAt(0).toUpperCase() || message.sender_email?.charAt(0).toUpperCase()}
                          </span>
                        </div>
                      )}
                      <div className="flex-1">
                        {!isMyMessage(message) && (
                          <p className="text-xs font-medium mb-1">
                            {message.sender_name || message.sender_email}
                          </p>
                        )}
                        <p className="text-sm">{message.content}</p>
                        <p className={`text-xs mt-1 ${
                          isMyMessage(message) ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          {formatTime(message.created_at)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="border-t border-gray-200 p-4 bg-white shadow-lg">
        <form onSubmit={sendMessage} className="flex space-x-3">
          <div className="flex-1">
            <input
              ref={inputRef}
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type a message... (Press Enter to send)"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none shadow-sm text-gray-900 placeholder:text-gray-400"
              disabled={sending}
            />
          </div>
          <button
            type="submit"
            disabled={!newMessage.trim() || sending}
            className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-300 disabled:to-gray-400 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-md hover:shadow-lg flex items-center gap-2"
          >
            {sending ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Sending...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                Send
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
