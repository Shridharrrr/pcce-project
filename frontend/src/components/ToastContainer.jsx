"use client";

import { createContext, useContext, useState, useCallback } from "react";
import Toast from "./Toast";

const ToastContext = createContext();

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "info", duration = 3000) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type, duration }]);
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const showSuccess = useCallback((message) => addToast(message, "success"), [addToast]);
  const showError = useCallback((message) => addToast(message, "error"), [addToast]);
  const showWarning = useCallback((message) => addToast(message, "warning"), [addToast]);
  const showInfo = useCallback((message) => addToast(message, "info"), [addToast]);

  const showConfirm = useCallback((message, onConfirm, onCancel) => {
    const id = Date.now();
    setToasts((prev) => [
      ...prev,
      {
        id,
        message,
        type: "confirm",
        duration: null,
        onConfirm,
        onCancel,
      },
    ]);
    return id;
  }, []);

  return (
    <ToastContext.Provider
      value={{
        addToast,
        removeToast,
        showSuccess,
        showError,
        showWarning,
        showInfo,
        showConfirm,
      }}
    >
      {children}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((toast) => (
          <div key={toast.id}>
            {toast.type === "confirm" ? (
              <div className="bg-blue-500 text-white rounded-lg shadow-lg p-4 min-w-[300px] max-w-md animate-slide-in">
                <p className="text-sm font-medium mb-3">{toast.message}</p>
                <div className="flex gap-2 justify-end">
                  <button
                    onClick={() => {
                      toast.onCancel?.();
                      removeToast(toast.id);
                    }}
                    className="px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded text-sm font-medium transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => {
                      toast.onConfirm?.();
                      removeToast(toast.id);
                    }}
                    className="px-3 py-1.5 bg-white text-blue-600 hover:bg-gray-100 rounded text-sm font-medium transition-colors"
                  >
                    Confirm
                  </button>
                </div>
              </div>
            ) : (
              <Toast
                message={toast.message}
                type={toast.type}
                duration={toast.duration}
                onClose={() => removeToast(toast.id)}
              />
            )}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};
