import { useEffect,useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";


export default function Courses(){

 const [courses,setCourses]=useState([])

 useEffect(()=>{
   loadCourses()
 },[])


 const loadCourses=async()=>{

   try{

    const res=
      await api.get(
        "/courses"
      )

    setCourses(
      res.data.courses
    )

   }catch(error){
     console.log(error)
   }

 }


 return(

<div className="page">

<h1 className="page-title">
Cursos Disponibles
</h1>

<div className="grid">

{
courses.map(course=>(

<div
 className="card"
 key={course.id}
>

<h2>
{course.name}
</h2>

<p>
{course.description}
</p>

<Link
to={`/courses/${course.id}/questions`}
className="primary-btn"
>
Ver preguntas
</Link>

</div>

))
}

</div>

</div>

)

}