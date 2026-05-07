import {
 BrowserRouter,
 Routes,
 Route
} from "react-router-dom";

import Login from "./pages/Login";
import Home from "./pages/Home";
import Courses from "./pages/Courses";
import CourseQuestions from "./pages/CourseQuestions";
import CreateQuestion from "./pages/CreateQuestion";
import QuestionDetail from "./pages/QuestionDetail";
import Register from "./pages/Register";


export default function App(){

 return(
  <BrowserRouter>

   <Routes>

    <Route
      path="/"
      element={<Login/>}
    />

    <Route
      path="/home"
      element={<Home/>}
    />

    <Route
      path="/courses"
      element={<Courses/>}
    />

    <Route
      path="/courses/:courseId/questions"
      element={<CourseQuestions/>}
    />

    <Route
      path="/courses/:courseId/create"
      element={<CreateQuestion/>}
    />

    <Route
      path="/questions/:questionId"
      element={<QuestionDetail/>}
    />

    <Route
        path="/register"
        element={<Register/>}
    />

   </Routes>

  </BrowserRouter>
 )
}