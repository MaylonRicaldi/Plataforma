import { useEffect, useState, useMemo } from "react";
import { auth } from "../app/firebase";
import api from "../services/api";
import Spinner from "../Spinner";
import "./Progress.css";

const NIVEL_EMOJI  = { bajo: "\ud83c\udf31", medio: "\ud83d\udcd8", alto: "\ud83d\udd25" };
const BLOOM_LABELS = ["", "Recordar", "Comprender", "Aplicar", "Analizar", "Evaluar", "Crear"];
const BLOOM_COLOR  = ["", "#94a3b8", "#60a5fa", "#34d399", "#f59e0b", "#f97316", "#a855f7"];

export default function Progress() {
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState("");

  useEffect(() => { loadProgress(); }, []);

  const loadProgress = async () => {
    try {
      const uid = auth.currentUser?.uid;
      const res = await api.get(`/progress${uid ? `?userId=${uid}` : ""}`);
      setData(res.data.result);
    } catch (err) {
      setError("No se pudo cargar el progreso");
    } finally {
      setLoading(false);
    }
  };

  const { totalPreguntas, nivelPromedio, nivelesDetalle, bloomPromedio, bloomDetalle, evolucion } = data || {};

  const barrasNivel = useMemo(() => {
    if (!nivelesDetalle || totalPreguntas === undefined) return [];
    return Object.entries(nivelesDetalle).map(([nivel, count]) => {
      const pct = totalPreguntas > 0 ? Math.round((count / totalPreguntas) * 100) : 0;
      return { nivel, count, pct };
    });
  }, [nivelesDetalle, totalPreguntas]);

  const bloomCards = useMemo(() => {
    if (!bloomDetalle || totalPreguntas === undefined) return [];
    return [1,2,3,4,5,6].map(lvl => {
      const count = bloomDetalle[lvl] || 0;
      const pct = totalPreguntas > 0 ? Math.round((count / totalPreguntas) * 100) : 0;
      return { lvl, count, pct };
    });
  }, [bloomDetalle, totalPreguntas]);

  if (loading) return <div className="progress-page"><Spinner text="Cargando tu progreso..." /></div>;
  if (error)   return <div className="progress-page"><p className="prog-error">{error}</p></div>;
  if (!data)   return null;

  return (
    <div className="progress-page">
      <div className="prog-header">
        <h1>Mi Progreso Académico</h1>
        <p>Evolución de la calidad de tus preguntas</p>
      </div>

      <div className="prog-kpis">
        <div className="prog-kpi">
          <span className="kpi-value">{totalPreguntas}</span>
          <span className="kpi-label">Preguntas realizadas</span>
        </div>
        <div className="prog-kpi">
          <span className="kpi-value">{(NIVEL_EMOJI[nivelPromedio] || "") + " " + nivelPromedio}</span>
          <span className="kpi-label">Nivel cognitivo promedio</span>
        </div>
        <div className="prog-kpi">
          <span className="kpi-value">{bloomPromedio > 0 ? bloomPromedio + "/6" : "\u2014"}</span>
          <span className="kpi-label">Bloom promedio</span>
        </div>
      </div>

      <div className="prog-section">
        <h2>Distribución por nivel cognitivo</h2>
        <div className="prog-bars">
          {barrasNivel.map(({ nivel, count, pct }) => (
            <div key={nivel} className="bar-row">
              <span className="bar-label">{NIVEL_EMOJI[nivel]} {nivel}</span>
              <div className="bar-track">
                <div className={"bar-fill bar-" + nivel} style={{ width: pct + "%" }} />
              </div>
              <span className="bar-pct">{count} ({pct}%)</span>
            </div>
          ))}
        </div>
      </div>

      <div className="prog-section">
        <h2>Distribución por niveles de Bloom</h2>
        <div className="bloom-grid">
          {bloomCards.map(({ lvl, count, pct }) => (
            <div key={lvl} className="bloom-card" style={{ borderTopColor: BLOOM_COLOR[lvl] }}>
              <div className="bloom-num" style={{ color: BLOOM_COLOR[lvl] }}>{lvl}</div>
              <div className="bloom-name">{BLOOM_LABELS[lvl]}</div>
              <div className="bloom-count">{count} preguntas</div>
              <div className="bloom-bar-track">
                <div className="bloom-bar-fill" style={{ width: pct + "%", background: BLOOM_COLOR[lvl] }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {evolucion && evolucion.length > 0 && (
        <div className="prog-section">
          <h2>Últimas preguntas registradas</h2>
          <div className="prog-timeline">
            {evolucion.map((item, i) => (
              <div key={item.id || i} className="timeline-item">
                <div className={"tl-dot tl-dot-" + item.nivel} />
                <div className="tl-body">
                  <span className={"tl-badge tl-" + item.nivel}>{NIVEL_EMOJI[item.nivel]} {item.nivel}</span>
                  {item.bloomLevel && (
                    <span className="tl-bloom">Bloom {item.bloomLevel} \u2014 {BLOOM_LABELS[item.bloomLevel]}</span>
                  )}
                  <span className="tl-fecha">{item.fecha ? new Date(item.fecha).toLocaleDateString("es-PE") : ""}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {totalPreguntas === 0 && (
        <div className="prog-empty">
          <p>Aún no tienes preguntas registradas.</p>
          <p>¡Empieza haciendo tu primera pregunta!</p>
        </div>
      )}
    </div>
  );
}
