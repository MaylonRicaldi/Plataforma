import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useNavigate, Link } from "react-router-dom";

import { auth } from "../app/firebase";
import api from "../services/api";
import "./Login.css";

export default function Login() {

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [error,setError] = useState("");
  const [loading,setLoading] = useState(false);

  const login = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const userCredential =
        await signInWithEmailAndPassword(auth, email, password);
      const token =
        await userCredential.user.getIdToken(true);
      //await api.get("/auth/me", {
      // headers: { Authorization: `Bearer ${token}` }
      //});
      navigate("/home");
    } catch(err) {
      setError("Credenciales incorrectas");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      {/* ── FONDO ILUSTRADO ── */}
      <div className="bg-scene">
        <svg width="100%" height="100%" viewBox="0 0 700 520"
          preserveAspectRatio="xMidYMid slice"
          xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#bae6fd"/>
              <stop offset="100%" stopColor="#e0f2fe"/>
            </linearGradient>
            <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#4ade80"/>
              <stop offset="100%" stopColor="#16a34a"/>
            </linearGradient>
          </defs>

          {/* Cielo */}
          <rect width="700" height="520" fill="url(#sky)"/>

          {/* Sol */}
          <circle cx="80" cy="70" r="44" fill="#fde68a" opacity="0.9"/>
          <circle cx="80" cy="70" r="34" fill="#fbbf24"/>
          <line x1="80" y1="14" x2="80" y2="4" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="80" y1="126" x2="80" y2="136" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="24" y1="70" x2="14" y2="70" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="136" y1="70" x2="146" y2="70" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="40" y1="30" x2="33" y2="23" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="120" y1="110" x2="127" y2="117" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="40" y1="110" x2="33" y2="117" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>
          <line x1="120" y1="30" x2="127" y2="23" stroke="#fbbf24" strokeWidth="4" strokeLinecap="round"/>

          {/* Nubes */}
          <g opacity="0.9">
            <ellipse cx="200" cy="80" rx="50" ry="26" fill="white"/>
            <ellipse cx="170" cy="90" rx="30" ry="20" fill="white"/>
            <ellipse cx="235" cy="88" rx="32" ry="19" fill="white"/>
          </g>
          <g opacity="0.85">
            <ellipse cx="560" cy="60" rx="44" ry="22" fill="white"/>
            <ellipse cx="534" cy="68" rx="26" ry="17" fill="white"/>
            <ellipse cx="590" cy="66" rx="28" ry="16" fill="white"/>
          </g>

          {/* Pasto */}
          <rect x="0" y="400" width="700" height="120" fill="url(#grass)"/>
          <path d="M0 400 Q87 380 175 400 Q262 420 350 400 Q437 380 525 400 Q612 420 700 400 L700 420 Q612 440 525 420 Q437 400 350 420 Q262 440 175 420 Q87 400 0 420 Z"
            fill="#22c55e" opacity="0.5"/>

          {/* Colegio */}
          <g transform="translate(30,270)">
            <rect x="0" y="60" width="120" height="130" fill="#fde68a"/>
            <polygon points="60,10 -10,65 130,65" fill="#ef4444"/>
            <line x1="60" y1="10" x2="60" y2="-20" stroke="#92400e" strokeWidth="3"/>
            <rect x="60" y="-20" width="30" height="18" fill="#ef4444"/>
            <rect x="42" y="135" width="36" height="55" rx="18" fill="#1d4ed8"/>
            <circle cx="60" cy="162" r="3" fill="#fbbf24"/>
            <rect x="10" y="80" width="30" height="28" rx="4" fill="#bae6fd"/>
            <rect x="80" y="80" width="30" height="28" rx="4" fill="#bae6fd"/>
            <rect x="10" y="118" width="30" height="20" rx="4" fill="#bae6fd"/>
            <rect x="80" y="118" width="30" height="20" rx="4" fill="#bae6fd"/>
            <rect x="20" y="60" width="80" height="18" rx="4" fill="#1d4ed8"/>
            <text x="60" y="73" textAnchor="middle" fontSize="9"
              fill="white" fontFamily="Nunito, sans-serif" fontWeight="800">
              COLEGIO
            </text>
          </g>

          {/* Árbol izquierda */}
          <g transform="translate(160,310)">
            <rect x="12" y="60" width="16" height="50" fill="#92400e"/>
            <circle cx="20" cy="40" r="32" fill="#16a34a"/>
            <circle cx="5" cy="50" r="22" fill="#22c55e"/>
            <circle cx="35" cy="50" r="22" fill="#22c55e"/>
            <circle cx="20" cy="22" r="20" fill="#4ade80"/>
          </g>

          {/* Árbol derecha */}
          <g transform="translate(520,300)">
            <rect x="12" y="60" width="16" height="60" fill="#92400e"/>
            <circle cx="20" cy="40" r="36" fill="#16a34a"/>
            <circle cx="2" cy="52" r="24" fill="#22c55e"/>
            <circle cx="38" cy="52" r="24" fill="#22c55e"/>
            <circle cx="20" cy="18" r="22" fill="#4ade80"/>
          </g>

          {/* Niño con mochila */}
          <g transform="translate(580,350)">
            <rect x="14" y="26" width="18" height="22" rx="4" fill="#7c3aed"/>
            <rect x="6" y="26" width="24" height="28" rx="6" fill="#3b82f6"/>
            <circle cx="18" cy="18" r="14" fill="#fcd34d"/>
            <ellipse cx="18" cy="6" rx="13" ry="5" fill="#92400e"/>
            <circle cx="13" cy="16" r="2" fill="#1e293b"/>
            <circle cx="23" cy="16" r="2" fill="#1e293b"/>
            <path d="M13 22 Q18 27 23 22" stroke="#b45309" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
            <line x1="6" y1="32" x2="-4" y2="44" stroke="#fcd34d" strokeWidth="6" strokeLinecap="round"/>
            <line x1="30" y1="32" x2="40" y2="44" stroke="#fcd34d" strokeWidth="6" strokeLinecap="round"/>
            <line x1="12" y1="54" x2="10" y2="70" stroke="#1e40af" strokeWidth="7" strokeLinecap="round"/>
            <line x1="24" y1="54" x2="26" y2="70" stroke="#1e40af" strokeWidth="7" strokeLinecap="round"/>
          </g>

          {/* Niña con libro */}
          <g transform="translate(90,355)">
            <rect x="6" y="24" width="24" height="28" rx="6" fill="#ec4899"/>
            <path d="M4 48 Q18 62 32 48" fill="#f9a8d4"/>
            <circle cx="18" cy="16" r="14" fill="#fcd34d"/>
            <ellipse cx="18" cy="4" rx="13" ry="5" fill="#1e293b"/>
            <circle cx="4" cy="10" r="6" fill="#1e293b"/>
            <circle cx="32" cy="10" r="6" fill="#1e293b"/>
            <circle cx="4" cy="10" r="3" fill="#f472b6"/>
            <circle cx="32" cy="10" r="3" fill="#f472b6"/>
            <circle cx="13" cy="14" r="2" fill="#1e293b"/>
            <circle cx="23" cy="14" r="2" fill="#1e293b"/>
            <path d="M13 20 Q18 25 23 20" stroke="#b45309" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
            <line x1="30" y1="30" x2="46" y2="40" stroke="#fcd34d" strokeWidth="6" strokeLinecap="round"/>
            <rect x="42" y="34" width="20" height="26" rx="3" fill="#3b82f6"/>
            <line x1="52" y1="34" x2="52" y2="60" stroke="white" strokeWidth="1"/>
            <line x1="6" y1="30" x2="-4" y2="42" stroke="#fcd34d" strokeWidth="6" strokeLinecap="round"/>
            <line x1="12" y1="58" x2="10" y2="74" stroke="#db2777" strokeWidth="7" strokeLinecap="round"/>
            <line x1="24" y1="58" x2="26" y2="74" stroke="#db2777" strokeWidth="7" strokeLinecap="round"/>
          </g>

        </svg>
      </div>

      {/* ── CARD DEL LOGIN ── */}
      <div className="login-card">

        <h1>
          Plataforma Inteligente
        </h1>

        <form onSubmit={login}>

          <label htmlFor="login-email" style={{display:"none"}}>Correo electrónico</label>
          <input
            id="login-email"
            type="email"
            placeholder="Correo"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="login-password" style={{display:"none"}}>Contraseña</label>
          <input
            id="login-password"
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Ingresando..." : "Ingresar"}
          </button>

          <Link to="/register" className="register-btn">
            Crear cuenta nueva
          </Link>

          {error && (
            <p className="error">{error}</p>
          )}

        </form>
      </div>

    </div>
  );
}