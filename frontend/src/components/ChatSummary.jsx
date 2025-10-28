"use client";

import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "./ToastContainer";

const ChatSummary = ({ selectedProject }) => {
  const { getIdToken } = useAuth();
  const { showSuccess, showError, showConfirm } = useToast();
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);
  const [expandedSummary, setExpandedSummary] = useState(null);

  // Function to format summary text
  const formatSummaryText = (text) => {
    if (!text) return null;
    
    // Remove all asterisks
    let formattedText = text.replace(/\*/g, '');
    
    // Split by lines
    const lines = formattedText.split('\n');
    
    return lines.map((line, index) => {
      let trimmedLine = line.trim();
      
      // Skip lines that are just "Summary:" or similar subheadings
      if (/^(summary|important points|key points|main topics):?\s*$/i.test(trimmedLine)) {
        return null;
      }
      
      // Remove "Summary:", "Important Points:", etc. from the beginning of lines
      trimmedLine = trimmedLine.replace(/^(summary|important points|key points|main topics):\s*/i, '');
      
      // Check if line is a heading (starts with a number followed by period)
      const isHeading = /^\d+\./.test(trimmedLine);
      
      if (!trimmedLine) {
        return <br key={index} />;
      }
      
      if (isHeading) {
        return (
          <p key={index} className="font-bold text-gray-900 mt-3 mb-1">
            {trimmedLine}
          </p>
        );
      }
      
      return (
        <p key={index} className="mb-1">
          {trimmedLine}
        </p>
      );
    });
  };

  useEffect(() => {
    if (selectedProject) {
      fetchSummaries();
    } else {
      setSummaries([]);
    }
  }, [selectedProject]);

  const fetchSummaries = async () => {
    if (!selectedProject) return;

    try {
      setLoading(true);
      setError(null);

      const token = await getIdToken();
      if (!token) throw new Error("No authentication token available");

      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.2:8000"
        }/summaries/team/${selectedProject.teamId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          setSummaries([]);
          return;
        }
        throw new Error(`Failed to fetch summaries: ${response.status}`);
      }

      const data = await response.json();
      setSummaries(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error fetching summaries:", err);
      setError(err.message || "Failed to load summaries");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSummary = async () => {
    if (!selectedProject) return;

    try {
      setGenerating(true);
      setError(null);

      const token = await getIdToken();
      if (!token) throw new Error("No authentication token available");

      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.2:8000"
        }/summaries/generate`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            team_id: selectedProject.teamId,
            message_count: 100,
          }),
        }
      );

      if (!response.ok) {
        let errorText;
        try {
          const errorJson = await response.json();
          errorText = errorJson.detail || JSON.stringify(errorJson);
        } catch {
          errorText = await response.text();
        }
        throw new Error(`Failed to generate summary: ${errorText}`);
      }

      const result = await response.json();
      console.log("Summary generated");

      // Refresh summaries list
      await fetchSummaries();
    } catch (err) {
      console.error("Error generating summary:", err);
      setError(err.message || "Failed to generate summary");
    } finally {
      setGenerating(false);
    }
  };

  const handleDeleteSummary = async (summaryId) => {
    showConfirm(
      "Are you sure you want to delete this summary?",
      async () => {
        try {
          await deleteSummaryAction(summaryId);
        } catch (err) {
          console.error("Error deleting summary:", err);
          showError(err.message || "Failed to delete summary");
        }
      }
    );
  };

  const deleteSummaryAction = async (summaryId) => {
    try {
      const token = await getIdToken();
      if (!token) throw new Error("No authentication token available");

      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.2:8000"
        }/summaries/${summaryId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to delete summary");
      }

      await fetchSummaries();
      showSuccess("Summary deleted successfully!");
    } catch (err) {
      throw err;
    }
  };

  if (!selectedProject) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Select a project to view chat summaries
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-50 overflow-hidden">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 flex-shrink-0">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-2xl font-bold text-gray-800">Chat Summaries</h2>
          <button
            onClick={handleGenerateSummary}
            disabled={generating}
            className={`px-4 py-2 rounded-lg transition-colors ${
              generating
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 text-white"
            }`}
          >
            {generating ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Generating...
              </span>
            ) : (
              "Generate Summary"
            )}
          </button>
        </div>
        <p className="text-sm text-gray-600">
          AI-powered summaries of your team conversations
        </p>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 m-4 rounded">
          {error}
        </div>
      )}

      {/* Summaries list */}
      <div className="flex-1 overflow-y-auto p-4">
        {summaries.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <p className="mb-4">
              No summaries yet. Generate your first summary!
            </p>
            <p className="text-sm text-gray-400">
              Summaries are generated using AI to help you quickly understand
              your team's conversations.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {summaries.map((summary) => (
              <div
                key={summary.summary_id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="flex items-center gap-2">
                    <div>
                      <p className="text-sm text-gray-700">
                        Generated on{" "}
                        {new Date(summary.created_at).toLocaleDateString()} at{" "}
                        {new Date(summary.created_at).toLocaleTimeString()}
                      </p>
                      <p className="text-xs text-gray-400">
                        By {summary.creator_email}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteSummary(summary.summary_id)}
                    className="text-red-600 hover:text-red-800 text-sm font-medium pr-4"
                  >
                    Delete
                  </button>
                </div>

                {/* Summary stats */}
                <div className="flex flex-wrap gap-2 mb-3">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                    {summary.total_messages} messages
                  </span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
                    {summary.participant_count} participants
                  </span>
                </div>

                {/* Gemini Summary */}
                <div className="bg-blue-50 py-4 px-6 mb-3 border border-purple-200">
                  <div className="flex items-center gap-2 mb-2">
                    <h4 className="font-bold text-blue-500 text-xl">
                      AI Generated Summary
                    </h4>
                  </div>
                  <div className="text-black font-sans leading-relaxed">
                    {formatSummaryText(summary.content)}
                  </div>
                </div>

                {/* Participants */}
                {summary.participants && summary.participants.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-500 mb-1">Participants:</p>
                    <div className="flex flex-wrap gap-1">
                      {summary.participants.map((participant, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                        >
                          {participant}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatSummary;
