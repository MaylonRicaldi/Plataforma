import { Link } from "react-router-dom";
import "./Home.css";

export default function Home() {
  return (
    <div className="home-page">

      <section className="hero">
        <div className="overlay" />
        <div className="hero-content">
          <h1>Plataforma Inteligente de Aprendizaje Basado en Preguntas</h1>
          <p>Crea preguntas, recibe retroalimentación con inteligencia artificial y fortalece tu pensamiento crítico.</p>
          <div className="hero-buttons">
            <Link to="/courses"  className="main-btn">Explorar Cursos</Link>
            <Link to="/progress" className="outline-btn">Ver mi Progreso</Link>
          </div>
        </div>
      </section>

      <section className="stats">
        <div className="stat-card"><h3>+100</h3><p>Preguntas creadas</p></div>
        <div className="stat-card"><h3>6</h3><p>Cursos activos</p></div>
        <div className="stat-card"><h3>IA</h3><p>Feedback automático</p></div>
        <div className="stat-card"><h3>6</h3><p>Niveles Bloom</p></div>
      </section>
    </div>
  );
}
