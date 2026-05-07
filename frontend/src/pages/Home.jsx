import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { signOut } from "firebase/auth";

import { auth } from "../app/firebase";

import "./Home.css";


export default function Home(){

const navigate=useNavigate()


const logout=async()=>{

await signOut(auth)

navigate("/")

}


return(

<div className="home-page">


{/* NAVBAR */}

<header className="navbar">

<div className="logo">
PreguntaIA
</div>


<nav>

<Link to="/home">
Inicio
</Link>

<Link to="/courses">
Cursos
</Link>

<Link to="/courses">
Haz una pregunta 
</Link>


<button
onClick={logout}
className="logout-btn"
>
Cerrar sesión
</button>

</nav>

</header>



{/* HERO */}

<section className="hero">


<div className="overlay"></div>


<div className="hero-content">

<h1>

Plataforma Inteligente
de Aprendizaje Basado
en Preguntas

</h1>


<p>

Crea preguntas,
recibe retroalimentación
con inteligencia artificial
y fortalece tu pensamiento crítico.

</p>



<div className="hero-buttons">

<Link
to="/courses"
className="main-btn"
>
Explorar Cursos
</Link>


<Link
to="/courses"
className="outline-btn"
>
Hacer Pregunta
</Link>

</div>


</div>

</section>




{/* SECCION INFERIOR */}

<section className="stats">

<div className="stat-card">
<h3>+100</h3>
<p>Preguntas creadas</p>
</div>

<div className="stat-card">
<h3>6</h3>
<p>Cursos activos</p>
</div>

<div className="stat-card">
<h3>IA</h3>
<p>Feedback automático</p>
</div>

</section>


</div>

)

}