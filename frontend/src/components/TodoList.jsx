"use client";

import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "./ToastContainer";
import ThemedLoader from "./ThemedLoader";

const TodoList = ({ selectedProject }) => {
  const { getIdToken, user } = useAuth();
  const { showSuccess, showError, showConfirm } = useToast();
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState("all");

  // Form state
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    deadline: "",
    priority: "medium",
    status: "pending",
    assigned_user_emails: [],
  });

  const [emailInput, setEmailInput] = useState("");

  useEffect(() => {
    if (selectedProject) {
      fetchTodos(true);
      // Auto-refresh every 3 seconds
      const intervalId = setInterval(() => {
        fetchTodos(false);
      }, 3000);
      return () => clearInterval(intervalId);
    } else {
      setTodos([]);
    }
  }, [selectedProject, getIdToken]);

  const fetchTodos = async (showLoader = true) => {
    if (!selectedProject) return;

    try {
      if (showLoader) setLoading(true);
      setError(null);

      const token = await getIdToken();
      if (!token) throw new Error("No authentication token available");

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.2:8000"}/todos/team/${selectedProject.teamId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          setTodos([]);
          return;
        }
        let errorText;
        try {
          const errorJson = await response.json();
          errorText = errorJson.detail || JSON.stringify(errorJson);
        } catch {
          errorText = await response.text();
        }
        console.error("Fetch error:", response.status, errorText);
        throw new Error(`Failed to fetch todos: ${errorText}`);
      }

      const data = await response.json();
      console.log("Fetched todos:", data);
      setTodos(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error fetching todos:", err);
      if (showLoader) setError(err.message || "Failed to load todos");
    } finally {
      if (showLoader) setLoading(false);
    }
  };

  const handleCreateTodo = async (e) => {
    e.preventDefault();

    try {
      const token = await getIdToken();
      if (!token) throw new Error("No authentication token available");

      const todoData = {
        ...formData,
        team_id: selectedProject.teamId,
        deadline: formData.deadline ? new Date(formData.deadline).toISOString() : null,
      };

      console.log("Creating todo:", todoData);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.2:8000"}/todos/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(todoData),
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
        console.error("Create error:", response.status, errorText);
        throw new Error(`Failed to create todo: ${errorText}`);
      }

      const result = await response.json();
      console.log("Create successful:", result);

      // Reset form and close modal
      resetForm();
      setShowCreateModal(false);
      await fetchTodos(true);
      showSuccess("Todo created successfully!");
    } catch (err) {
      console.error("Error creating todo:", err);
      showError(err.message || "Failed to create todo");
    }
  };

  const handleDeleteTodo = async (todoId) => {
    showConfirm(
      "Are you sure you want to delete this todo?",
      async () => {
        try {
          await deleteTodoAction(todoId);
        } catch (err) {
          console.error("Error deleting todo:", err);
          showError(err.message || "Failed to delete todo");
        }
      }
    );
  };

  const deleteTodoAction = async (todoId) => {
    try {
      const token = await getIdToken();
      if (!token) throw new Error("No authentication token available");

      console.log("Deleting todo:", todoId);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.2:8000"}/todos/${todoId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
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
        console.error("Delete error:", response.status, errorText);
        throw new Error(`Failed to delete todo: ${errorText}`);
      }

      console.log("Delete successful");
      await fetchTodos(true);
      showSuccess("Todo deleted successfully!");
    } catch (err) {
      throw err;
    }
  };

  const resetForm = () => {
    setFormData({
      title: "",
      description: "",
      deadline: "",
      priority: "medium",
      status: "pending",
      assigned_user_emails: [],
    });
    setEmailInput("");
  };

  const addEmail = () => {
    if (emailInput && !formData.assigned_user_emails.includes(emailInput)) {
      setFormData({
        ...formData,
        assigned_user_emails: [...formData.assigned_user_emails, emailInput],
      });
      setEmailInput("");
    }
  };

  const removeEmail = (email) => {
    setFormData({
      ...formData,
      assigned_user_emails: formData.assigned_user_emails.filter((e) => e !== email),
    });
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case "urgent":
        return "bg-red-100 text-red-800 border-red-300";
      case "high":
        return "bg-orange-100 text-orange-800 border-orange-300";
      case "medium":
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
      case "low":
        return "bg-green-100 text-green-800 border-green-300";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800 border-green-300";
      case "in_progress":
        return "bg-blue-100 text-blue-800 border-blue-300";
      case "cancelled":
        return "bg-gray-100 text-gray-800 border-gray-300";
      default:
        return "bg-yellow-100 text-yellow-800 border-yellow-300";
    }
  };

  const isOverdue = (todo) => {
    if (!todo.deadline || todo.status === "completed" || todo.status === "cancelled") {
      return false;
    }
    return new Date(todo.deadline) < new Date();
  };

  const filteredTodos = todos.filter((todo) => {
    if (filterStatus === "all") return true;
    return todo.status === filterStatus;
  });

  if (!selectedProject) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Select a project to view todos
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full bg-white">
        <ThemedLoader size="md" text="Loading todos..." />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Todo List</h2>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-500 transition-colors"
          >
            + Add Todo
          </button>
        </div>

        {/* Filter buttons */}
        <div className="flex gap-2">
          {["all", "pending", "in_progress", "completed"].map((status) => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                filterStatus === status
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              {status.replace("_", " ").toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 m-4 rounded">
          {error}
        </div>
      )}

      {/* Todo list */}
      <div className="flex-1 overflow-y-auto p-4">
        {filteredTodos.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            No todos found. Create one to get started!
          </div>
        ) : (
          <div className="space-y-3">
            {filteredTodos.map((todo) => (
              <div
                key={todo.todo_id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-semibold text-gray-800">{todo.title}</h3>
                  <button
                    onClick={() => handleDeleteTodo(todo.todo_id)}
                    className="text-red-600 hover:text-red-800 text-sm font-medium"
                  >
                    Delete
                  </button>
                </div>

                {todo.description && (
                  <p className="text-gray-600 text-sm mb-3">{todo.description}</p>
                )}

                <div className="flex flex-wrap gap-2 mb-3">
                  <span className={`px-2 py-1 rounded text-xs font-medium border ${getPriorityColor(todo.priority)}`}>
                    {todo.priority.toUpperCase()}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs font-medium border ${getStatusColor(todo.status)}`}>
                    {todo.status.replace("_", " ").toUpperCase()}
                  </span>
                  {todo.deadline && (
                    <span className={`px-2 py-1 rounded text-xs font-medium border ${
                      isOverdue(todo)
                        ? "bg-red-100 text-red-800 border-red-300 font-bold"
                        : "bg-purple-100 text-purple-800 border-purple-300"
                    }`}>
                      {isOverdue(todo) ? "⚠️ OVERDUE" : "Due"}: {new Date(todo.deadline).toLocaleDateString()}
                    </span>
                  )}
                </div>

                {todo.assigned_users.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-gray-500 mb-1">Assigned to:</p>
                    <div className="flex flex-wrap gap-1">
                      {todo.assigned_users.map((user) => (
                        <span
                          key={user.user_id}
                          className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                        >
                          {user.name}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-2 text-xs text-gray-400">
                  Created by {todo.creator_name} on {new Date(todo.created_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-white flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg border border-gray-200 shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Create New Todo</h2>
              <button
                onClick={() => {
                  setShowCreateModal(false);
                  resetForm();
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleCreateTodo} className="p-6 space-y-4">
              {/* Title */}
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  id="title"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Enter todo title"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-900 placeholder:text-gray-400"
                />
              </div>

              {/* Description */}
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Enter description (optional)"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none text-gray-900 placeholder:text-gray-400"
                />
              </div>

              {/* Deadline */}
              <div>
                <label htmlFor="deadline" className="block text-sm font-medium text-gray-700 mb-2">
                  Deadline
                </label>
                <input
                  type="datetime-local"
                  id="deadline"
                  value={formData.deadline}
                  onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-900"
                />
              </div>

              {/* Priority and Status in a row */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                    Priority
                  </label>
                  <select
                    id="priority"
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-900"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
                    Status
                  </label>
                  <select
                    id="status"
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-900"
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              {/* Assign to */}
              <div>
                <label htmlFor="assignEmail" className="block text-sm font-medium text-gray-700 mb-2">
                  Assign to
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="email"
                    id="assignEmail"
                    value={emailInput}
                    onChange={(e) => setEmailInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), addEmail())}
                    placeholder="user@example.com"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-900 placeholder:text-gray-400"
                  />
                  <button
                    type="button"
                    onClick={addEmail}
                    className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Add
                  </button>
                </div>
                {formData.assigned_user_emails.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {formData.assigned_user_emails.map((email) => (
                      <span
                        key={email}
                        className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm flex items-center gap-1"
                      >
                        {email}
                        <button
                          type="button"
                          onClick={() => removeEmail(email)}
                          className="text-blue-600 hover:text-blue-800 font-bold"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  Add team members by email address
                </p>
              </div>

              {/* Actions */}
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!formData.title.trim()}
                  className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span className="text-sm">Create Todo</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TodoList;
