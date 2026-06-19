import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import NotFound from "./pages/NotFound";
import Layout from "./Layout";

const Login           = lazy(() => import("./pages/Login"));
const Register        = lazy(() => import("./pages/Register"));
const Home            = lazy(() => import("./pages/Home"));
const Courses         = lazy(() => import("./pages/Courses"));
const CourseQuestions = lazy(() => import("./pages/CourseQuestions"));
const CreateQuestion  = lazy(() => import("./pages/CreateQuestion"));
const QuestionDetail  = lazy(() => import("./pages/QuestionDetail"));
const Progress        = lazy(() => import("./pages/Progress"));

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={
        <div style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          background: "#eef2ff",
        }}>
          <div className="app-spinner" />
          <style>{`.app-spinner{width:48px;height:48px;border:5px solid #e5e7eb;border-top:5px solid #2563eb;border-radius:50%;animation:spin 0.8s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}`}</style>
        </div>
      }>
        <Routes>
          <Route path="/"                               element={<Login />} />
          <Route path="/register"                       element={<Register />} />
          <Route element={<Layout />}>
            <Route path="/home"                         element={<Home />} />
            <Route path="/courses"                      element={<Courses />} />
            <Route path="/courses/:courseId/questions"  element={<CourseQuestions />} />
            <Route path="/courses/:courseId/create"     element={<CreateQuestion />} />
            <Route path="/questions/:questionId"        element={<QuestionDetail />} />
            <Route path="/progress"                     element={<Progress />} />
          </Route>
          <Route path="*"                               element={<NotFound />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
