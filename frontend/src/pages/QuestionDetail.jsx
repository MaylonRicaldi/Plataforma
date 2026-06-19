import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";
import Spinner from "../Spinner";
import "./QuestionDetail.css";

const BLOOM_LABEL = ["","Recordar","Comprender","Aplicar","Analizar","Evaluar","Crear"];
const NIVEL_EMOJI = { bajo: "🌱", medio: "📘", alto: "🔥" };

export default function QuestionDetail() {
  const { questionId } = useParams();
  const [question, setQuestion] = useState(null);

  useEffect(() => { loadDetail(); }, []);

  const loadDetail = async () => {
    try {
      const res = await api.get(`/questions/${questionId}`);
      setQuestion(res.data.question);
    } catch (error) {
      // Error manejado por el estado: question permanece null
    }
  };

  if (!question) return <Spinner text="Cargando pregunta..." />;

  const bloomIdx = question.bloomLevel;

  return (
    <div className="detail-page">
      <div className="detail-card">
        <h1>{question.questionText}</h1>

        <div className="detail-box">
          <h3>Autor</h3>
          <p>{question.userName}</p>
        </div>

        <div className="detail-box">
          <h3>Nivel Cognitivo</h3>
          <p>{NIVEL_EMOJI[question.aiLevel]} {question.aiLevel}
            {bloomIdx && <span style={{marginLeft:8, opacity:0.7, fontSize:13}}>
              (Bloom {bloomIdx}/6 — {BLOOM_LABEL[bloomIdx]})
            </span>}
          </p>
        </div>

        {question.cursoDetectado && (
          <div className="detail-box">
            <h3>Curso detectado</h3>
            <p>{question.cursoDetectado}</p>
          </div>
        )}

        <div className="detail-box">
          <h3>Feedback de IA</h3>
          <p>{question.aiFeedback}</p>
        </div>

        <div className="detail-box">
          <h3>Pregunta Mejorada</h3>
          <p>{question.improvedQuestion}</p>
        </div>

        <Link to={`/courses/${question.courseId}/questions`}
          style={{display:"inline-block", marginTop:16, color:"#6366f1", fontWeight:800, textDecoration:"none"}}>
          ← Volver al curso
        </Link>
      </div>
    </div>
  );
}
