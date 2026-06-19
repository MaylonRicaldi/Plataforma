import { createContext, useContext, useState, useCallback } from "react";

const ToastContext = createContext(null);

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "info", duration = 3000) => {
    const id = ++toastId;
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, duration);
  }, []);

  return (
    <ToastContext.Provider value={addToast}>
      {children}
      <div style={{
        position: "fixed",
        top: "20px",
        right: "20px",
        zIndex: 9999,
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}>
        {toasts.map(t => (
          <div key={t.id} style={{
            padding: "14px 20px",
            borderRadius: "12px",
            color: "white",
            fontWeight: 600,
            fontFamily: "Nunito, sans-serif",
            fontSize: "15px",
            boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
            background: t.type === "success" ? "#16a34a" :
                        t.type === "error" ? "#dc2626" :
                        t.type === "warning" ? "#f59e0b" : "#2563eb",
            animation: "slideIn 0.3s ease",
            maxWidth: "360px",
          }}>
            {t.message}
          </div>
        ))}
      </div>
      <style>{`
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}
