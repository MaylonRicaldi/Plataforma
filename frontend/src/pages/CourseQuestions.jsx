import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../services/api";
import Spinner from "../Spinner";
import "./CourseQuestions.css";

export default function CourseQuestions() {

  const { courseId } = useParams();

  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadQuestions();
  }, [courseId]);

  const loadQuestions = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get(`/courses/${courseId}/questions`);
      setQuestions(res.data.questions);
    } catch (error) {
      setError("No se pudieron cargar las preguntas");
    } finally {
      setLoading(false);
    }
  };

  return (
<div className="questions-page">
<div className="questions-header">
<h1>Preguntas del Curso</h1>
<Link to={`/courses/${courseId}/create`} className="create-btn">
+ Crear Pregunta
</Link>
</div>

{loading && <Spinner text="Cargando preguntas..." />}
{error && <p className="questions-empty" style={{color:"#dc2626"}}>{error}</p>}
{!loading && !error && questions.length===0 && <p className="questions-empty">No hay preguntas todavía.</p>}

<div className="questions-grid">
{questions.map((item)=>(
<Link key={item.id} to={`/questions/${item.id}`} className="question-card">
<h3>{item.questionText}</h3>
<p>Autor: {item.userName || "---"}</p>
</Link>
))}
</div>

</div>
)
}