import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import api from "../services/api";
import { auth } from "../app/firebase";
import { useToast } from "../ToastContext";
import "./CreateQuestion.css";


export default function CreateQuestion() {

  const navigate = useNavigate();
  const toast = useToast();

  const { courseId } = useParams();

  const [questionText, setQuestionText] = useState("");
  const [loading, setLoading] = useState(false);

  const submitQuestion = async (e) => {
    e.preventDefault();
    if (!questionText.trim()) {
      toast("Escribe una pregunta", "warning");
      return;
    }

    const currentUser = auth.currentUser;
    if (!currentUser) {
      toast("Debes iniciar sesión", "error");
      return;
    }

    setLoading(true);

    try {
      const response = await api.post("/questions", {
        courseId: courseId,
        questionText: questionText,
        userId: currentUser.uid,
        userName: currentUser.email
      });

      toast("Pregunta creada y analizada correctamente", "success");

      setTimeout(() => {
        navigate(`/courses/${courseId}/questions`);
      }, 1000);

    } catch (error) {
      toast("No se pudo guardar la pregunta", "error");
    } finally {
      setLoading(false);
    }
  };



  return (

    <div className="page form-page">

      <div className="deco-circle" />

      <h1 className="page-title">
        💡 Crear Pregunta
      </h1>

      <p className="page-subtitle">
        La IA analizará tu pregunta automáticamente
      </p>

      <div className="form-tips">
        <div className="form-tip"><span>🎯</span> Sé específico</div>
        <div className="form-tip"><span>🧠</span> Invita a reflexionar</div>
        <div className="form-tip"><span>📖</span> Usa el tema del curso</div>
      </div>

      <form
        onSubmit={submitQuestion}
        className="form-card"
      >

        <label className="form-label">
          Escribe tu pregunta:
        </label>


        <textarea
          rows="6"
          placeholder="Ejemplo: ¿Por qué es importante la fotosíntesis?"
          value={questionText}
          onChange={(e) =>
            setQuestionText(
              e.target.value
            )
          }
        />

        <div className="ai-badge">
          <div className="ai-badge-icon">🤖</div>
          <div className="ai-badge-text">
            <strong>Análisis automático con IA</strong>
            Tu pregunta recibirá un nivel cognitivo y sugerencias de mejora
          </div>
        </div>

        <div className="form-divider">lista para enviar</div>

        <button
          type="submit"
          className="primary-btn"
          disabled={loading}
        >

          {
            loading
              ? "⏳ Analizando con IA..."
              : "🚀 Guardar pregunta"
          }

        </button>

      </form>

    </div>

  )

}