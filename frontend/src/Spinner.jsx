export default function Spinner({ text = "Cargando..." }) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "60px 20px",
      gap: "16px",
      fontFamily: "Nunito, sans-serif",
      color: "#6b7280",
      fontSize: "16px",
    }}>
      <div className="spinner" />
      <style>{`
        .spinner {
          width: 40px;
          height: 40px;
          border: 4px solid #e5e7eb;
          border-top: 4px solid #2563eb;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
      {text}
    </div>
  );
}
