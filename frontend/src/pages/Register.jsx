import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "./Auth.css";

export default function Register() {

  const navigate = useNavigate();
  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState("");

  const registerUser = async (e) => {
    e.preventDefault();
    setError("");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Ingresa un correo electronico valido");
      return;
    }
    if (password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres");
      return;
    }
    if (!/[A-Z]/.test(password)) {
      setError("La contraseña debe contener al menos una mayuscula");
      return;
    }
    if (!/\d/.test(password)) {
      setError("La contraseña debe contener al menos un numero");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/auth/register", { email, password });
      const data = res.data;

      if (!data.success) {
        setError(data.message || "Error al crear usuario");
        return;
      }

      navigate("/");
    } catch (error) {
      const msg = error.response?.data?.message || "Error de conexion con el servidor";
      setError(msg);
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
          required
        />

        <input
          type="password"
          placeholder="Contraseña minimo 8 caracteres, 1 mayuscula, 1 numero)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
        />

        {error && <p className="error" style={{ color: "#dc2626", marginBottom: "12px", fontSize: "14px" }}>{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Creando..." : "Registrarse"}
        </button>

      </form>
    </div>
  );
}