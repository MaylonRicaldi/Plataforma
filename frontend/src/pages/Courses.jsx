import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import Spinner from "../Spinner";
import "./Courses.css";

export default function Courses(){
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(()=>{
    loadCourses()
  },[])

  const loadCourses = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/courses")
      setCourses(res.data.courses)
    } catch(error) {
      setError("No se pudieron cargar los cursos")
    } finally {
      setLoading(false);
    }
  }

  return(
    <div className="page">
      <h1 className="page-title">Cursos Disponibles</h1>
      {loading && <Spinner text="Cargando cursos..." />}
      {error && <p style={{textAlign:"center",color:"#dc2626"}}>{error}</p>}
      {!loading && !error && courses.length === 0 && <p style={{textAlign:"center",color:"#6b7280"}}>No hay cursos disponibles.</p>}
      <div className="grid">
        {courses.map(course=>(
          <div className="card" key={course.id}>
            <h2>{course.name}</h2>
            <p>{course.description}</p>
            <Link to={`/courses/${course.id}/questions`} className="primary-btn">
              Ver preguntas
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}
