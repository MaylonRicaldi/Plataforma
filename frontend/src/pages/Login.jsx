import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useNavigate, Link } from "react-router-dom";

import { auth } from "../app/firebase";
import api from "../services/api";


export default function Login() {

  const navigate = useNavigate();

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [error,setError] = useState("");
  const [loading,setLoading] = useState(false);


  const login = async (e) => {

    e.preventDefault();

    setError("");
    setLoading(true);

    try{

      const userCredential =
      await signInWithEmailAndPassword(
        auth,
        email,
        password
      );


      // fuerza token fresco
      const token =
      await userCredential.user.getIdToken(
        true
      );


      await api.get(
        "/auth/me",
        {
          headers:{
            Authorization:
            `Bearer ${token}`
          }
        }
      );


      navigate(
        "/home"
      );

    }

    catch(err){

      console.error(err);

      setError(
        "Credenciales incorrectas"
      );

    }

    finally{

      setLoading(false);

    }

  };



  return(

    <div className="login-page">

      <div className="login-card">

        <h1>
          Plataforma Inteligente
        </h1>


        <form onSubmit={login}>

          <input
            type="email"
            placeholder="Correo"
            value={email}
            onChange={(e)=>
              setEmail(
                e.target.value
              )
            }
            required
          />


          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e)=>
              setPassword(
                e.target.value
              )
            }
            required
          />


          <button
            type="submit"
            disabled={loading}
          >
            {
              loading
              ? "Ingresando..."
              : "Ingresar"
            }
          </button>



          <Link
            to="/register"
            className="register-btn"
          >
            Crear cuenta nueva
          </Link>



          {error && (

            <p className="error">
              {error}
            </p>

          )}


        </form>

      </div>

    </div>

  )

}