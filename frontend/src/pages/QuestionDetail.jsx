import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

import "./QuestionDetail.css";


export default function QuestionDetail(){

const { questionId } = useParams();

const [question,setQuestion] = useState(null);



useEffect(()=>{

loadDetail();

},[])



const loadDetail = async ()=>{

try{

const res = await api.get(
`/questions/${questionId}`
);

setQuestion(
res.data.question
)

}
catch(error){

console.error(error)

}

}



if(!question){
return <p>Cargando...</p>
}



return(

<div className="detail-page">

<div className="detail-card">

<h1>
{question.questionText}
</h1>


<div className="detail-box">

<h3>
Autor
</h3>

<p>
{question.userName}
</p>

</div>



<div className="detail-box">

<h3>
Nivel Cognitivo
</h3>

<p>
{question.aiLevel}
</p>

</div>



<div className="detail-box">

<h3>
Feedback de IA
</h3>

<p>
{question.aiFeedback}
</p>

</div>



<div className="detail-box">

<h3>
Pregunta Mejorada
</h3>

<p>
{question.improvedQuestion}
</p>

</div>


</div>

</div>

)

}