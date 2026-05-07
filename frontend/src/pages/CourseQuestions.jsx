import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../services/api";

import "./CourseQuestions.css";

export default function CourseQuestions() {

  const { courseId } = useParams();

  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);



  useEffect(() => {

    loadQuestions();

  }, []);



  const loadQuestions = async () => {

    try {

      const res = await api.get(
        `/courses/${courseId}/questions`
      );

      setQuestions(
        res.data.questions
      );

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }

  };



  return (

<div className="questions-page">

<div className="questions-header">

<h1>
Preguntas del Curso
</h1>

<Link
to={`/courses/${courseId}/create`}
className="create-btn"
>
+ Crear Pregunta
</Link>

</div>



{
loading &&
<p>Cargando preguntas...</p>
}



{
!loading &&
questions.length===0 &&
<p>No hay preguntas todavía.</p>
}



<div className="questions-grid">

{
questions.map((item)=>(

<Link
key={item.id}
to={`/questions/${item.id}`}
className="question-card"
>

<h3>
{item.questionText}
</h3>

<p>
Autor:
{item.userName}
</p>

</Link>

))
}

</div>


</div>

)

}