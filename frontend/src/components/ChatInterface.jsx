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
      fetchMessages();
    } else {
      setMessages([]);
    }
  }, [selectedProject]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchMessages = async () => {
    if (!selectedProject) return;

    try {
      setLoading(true);
      setError(null);
      
      const token = await getIdToken();
      
      if (!token) {
        throw new Error('No authentication token available');
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/messages/${selectedProject.teamId}`,
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
        throw new Error(`Failed to fetch messages: ${response.status}`);
      }

      const data = await response.json();
      setMessages(data);
    } catch (err) {
      console.error('Error fetching messages:', err);
      setError(err.message || 'Failed to load messages');
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedProject || sending) return;

    try {
      setSending(true);
      setError(null);
      
      const token = await getIdToken();
      
      if (!token) {
        throw new Error('No authentication token available');
      }
      
      const messageData = {
        team_id: selectedProject.teamId,
        content: newMessage.trim(),
        message_type: "text",
        metadata: {}
      };

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/messages/`,
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
      setNewMessage("");
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message');
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
      <div className="flex-1 bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Project</h3>
          <p className="text-gray-500">Choose a project from the sidebar to start chatting</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 bg-white flex flex-col">
      {/* Chat Header */}
      <div className="border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">{selectedProject.teamName}</h2>
            <p className="text-sm text-gray-500">
              {selectedProject.members?.length} member{selectedProject.members?.length !== 1 ? 's' : ''}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex -space-x-1">
              {selectedProject.members?.slice(0, 4).map((member, index) => (
                <div
                  key={index}
                  className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center border-2 border-white"
                >
                  <span className="text-white text-sm font-medium">
                    {member.name?.charAt(0).toUpperCase() || member.email?.charAt(0).toUpperCase()}
                  </span>
                </div>
              ))}
              {selectedProject.members?.length > 4 && (
                <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center border-2 border-white">
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
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
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
                  <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    isMyMessage(message)
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    <div className="flex items-start space-x-2">
                      {!isMyMessage(message) && (
                        <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
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
      <div className="border-t border-gray-200 p-4">
        <form onSubmit={sendMessage} className="flex space-x-3">
          <div className="flex-1">
            <input
              ref={inputRef}
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              placeholder="Type a message..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              disabled={sending}
            />
          </div>
          <button
            type="submit"
            disabled={!newMessage.trim() || sending}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
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
