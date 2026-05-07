import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Auth.css";

export default function Register() {

  const navigate = useNavigate();
  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]   = useState(false);

  const registerUser = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Llama a TU backend, no a Firebase directamente
      const res = await fetch("http://localhost:5000/api/auth/register", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!data.success) {
        alert(data.error || "Error al crear usuario");
        return;
      }

      alert("Usuario creado correctamente");
      navigate("/");

    } catch (error) {
      alert("Error de conexión con el servidor");
      console.error(error);

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <form onSubmit={registerUser} className="auth-card">

        <h1>Crear Cuenta</h1>

        <input
          type="email"
          placeholder="Correo"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button disabled={loading}>
          {loading ? "Creando..." : "Registrarse"}
        </button>

      </form>
    </div>
  );
}