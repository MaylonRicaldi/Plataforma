import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
          padding: "40px",
          textAlign: "center",
          fontFamily: "Nunito, sans-serif",
          background: "#eef2ff",
        }}>
          <h1 style={{ fontSize: "48px", color: "#1e3a8a", marginBottom: "20px" }}>
            Algo salió mal
          </h1>
          <p style={{ fontSize: "18px", color: "#4b5563", marginBottom: "30px" }}>
            Ocurrió un error inesperado. Por favor, recarga la página.
          </p>
          <button
            onClick={() => window.location.reload()}
            style={{
              padding: "14px 28px",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "12px",
              fontSize: "16px",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            Recargar página
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
