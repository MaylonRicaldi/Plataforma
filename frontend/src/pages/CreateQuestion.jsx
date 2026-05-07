import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import api from "../services/api";
import { auth } from "../app/firebase";


export default function CreateQuestion() {

  const navigate = useNavigate();

  const { courseId } = useParams();

  const [questionText, setQuestionText] = useState("");

  const [loading, setLoading] = useState(false);



  const submitQuestion = async (e) => {

    e.preventDefault();

    if (!questionText.trim()) {
      alert("Escribe una pregunta");
      return;
    }


    const currentUser = auth.currentUser;

    if (!currentUser) {
      alert("Debes iniciar sesión");
      return;
    }


    setLoading(true);

    try {

      const response = await api.post(
        "/questions",
        {
          courseId: courseId,

          questionText: questionText,

          userId: currentUser.uid,

          userName: currentUser.email
        }
      );


      console.log(
        response.data
      );


      alert(
        "Pregunta creada y analizada correctamente"
      );


      setTimeout(() => {

        navigate(
          `/courses/${courseId}/questions`
        )

      }, 1000);



    } catch (error) {

      console.error(
        error
      );

      alert(
        "No se pudo guardar la pregunta"
      );

    }

    finally {

      setLoading(false);

    }

  };



  return (

    <div className="page form-page">

      <h1 className="page-title">
        Crear Pregunta
      </h1>


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


        <button
          type="submit"
          className="primary-btn"
          disabled={loading}
        >

          {
            loading
              ? "Analizando con IA..."
              : "Guardar pregunta"
          }

        </button>

      </form>

    </div>

  )

}