from flask import Flask
from flask_cors import CORS

from src.adapters.inbound.controllers.AuthController import router as auth_router
from src.adapters.inbound.controllers.CourseController import router as course_router
from src.adapters.inbound.controllers.CrearPreguntaController import router as crear_pregunta_router
from src.adapters.inbound.controllers.EvaluarPreguntaController import router as evaluar_pregunta_router
from src.adapters.inbound.controllers.MejorarPreguntaController import router as mejorar_pregunta_router
from src.adapters.inbound.controllers.QuestionController import router as question_router


app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_router)
app.register_blueprint(course_router)
app.register_blueprint(crear_pregunta_router)
app.register_blueprint(evaluar_pregunta_router)
app.register_blueprint(mejorar_pregunta_router)
app.register_blueprint(question_router)


@app.route("/")
def home():
    return {
        "success": True,
        "message": "Backend funcionando correctamente"
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)
