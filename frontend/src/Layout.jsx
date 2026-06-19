import { Link, Outlet, useNavigate } from "react-router-dom";
import { signOut } from "firebase/auth";
import { auth } from "./app/firebase";

export default function Layout() {
  const navigate = useNavigate();

  const logout = async () => {
    await signOut(auth);
    navigate("/");
  };

  return (
    <div>
      <header style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "16px 40px",
        background: "white",
        boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}>
        <Link to="/home" style={{
          fontSize: "24px",
          fontWeight: 900,
          color: "#2563eb",
          textDecoration: "none",
          fontFamily: "'Fredoka One', cursive",
        }}>
          PreguntaIA
        </Link>
        <nav style={{
          display: "flex",
          gap: "24px",
          alignItems: "center",
          flexWrap: "wrap",
        }}>
          <Link to="/home" style={navLinkStyle} aria-label="Ir a inicio">Inicio</Link>
          <Link to="/courses" style={navLinkStyle} aria-label="Ir a cursos">Cursos</Link>
          <Link to="/progress" style={navLinkStyle} aria-label="Ir a mi progreso">Mi Progreso</Link>
          <button onClick={logout} aria-label="Cerrar sesión" style={{
            padding: "8px 18px",
            background: "#ef4444",
            color: "white",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
            fontWeight: 600,
            fontSize: "14px",
            fontFamily: "Nunito, sans-serif",
          }}>
            Cerrar sesión
          </button>
        </nav>
      </header>
      <Outlet />
    </div>
  );
}

const navLinkStyle = {
  textDecoration: "none",
  color: "#374151",
  fontWeight: 600,
  fontSize: "15px",
  fontFamily: "Nunito, sans-serif",
};
