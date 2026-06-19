import { Link } from "react-router-dom";

export default function NotFound() {
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
      <h1 style={{ fontSize: "80px", color: "#2563eb", marginBottom: "10px" }}>404</h1>
      <h2 style={{ fontSize: "28px", color: "#1e3a8a", marginBottom: "20px" }}>
        Página no encontrada
      </h2>
      <p style={{ fontSize: "18px", color: "#4b5563", marginBottom: "30px" }}>
        La página que buscas no existe o ha sido movida.
      </p>
      <Link
        to="/"
        style={{
          padding: "14px 28px",
          background: "#2563eb",
          color: "white",
          textDecoration: "none",
          borderRadius: "12px",
          fontSize: "16px",
          fontWeight: "bold",
        }}
      >
        Volver al inicio
      </Link>
    </div>
  );
}
