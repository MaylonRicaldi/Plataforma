import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone

from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from werkzeug.exceptions import BadRequest, HTTPException

logging.basicConfig(
    level=logging.DEBUG if os.getenv("FLASK_DEBUG", "0") == "1" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

from src.infrastructure.adapters.inbound.controllers.auth_controller     import router as auth_router
from src.infrastructure.adapters.inbound.controllers.course_controller   import router as course_router
from src.infrastructure.adapters.inbound.controllers.question_controller import router as question_router
from src.infrastructure.adapters.inbound.controllers.ai_controller       import router as ai_router
from src.infrastructure.adapters.inbound.controllers.progress_controller import router as progress_router

from src.infrastructure.config.di_container import container
from src.infrastructure.adapters.outbound.database.FirestoreRepository import FirestoreRepository
from src.infrastructure.adapters.outbound.ai.NLPServiceAdapter import NLPServiceAdapter
from src.infrastructure.adapters.outbound.analytics.AnalyticsAdapter import AnalyticsAdapter



def create_app() -> Flask:
    app = Flask(__name__)

    log_dir = os.getenv("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "preguntaia.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG if os.getenv("FLASK_DEBUG", "0") == "1" else logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logging.getLogger("").addHandler(file_handler)

    @app.after_request
    def add_security_headers(response):
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' fonts.googleapis.com 'unsafe-inline'; "
            "font-src fonts.gstatic.com; "
            "connect-src 'self' https://*.firebaseio.com https://*.googleapis.com https://*.firebase.com; "
            "img-src 'self' data:; "
            "frame-src 'none'; "
            "object-src 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        return response

    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    repo = FirestoreRepository()
    nlp = NLPServiceAdapter()
    analytics = AnalyticsAdapter()
    container.init_app(repository=repo, nlp_service=nlp, analytics=analytics)
    logger.info("Dependencias registradas en el contenedor DI")

    redis_url = os.getenv("REDIS_URL")
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["1000 per day", "200 per hour"],
        storage_uri=redis_url or "memory://",
    )
    if redis_url:
        logger.info("Rate limiter usando Redis: %s", redis_url)
    else:
        logger.info("Rate limiter usando memoria (no persiste entre reinicios)")

    if os.getenv("FLASK_ENV", "development") != "production":
        Swagger(app, template={
            "swagger": "2.0",
            "info": {
                "title": "PreguntaIA API",
                "description": "API de la Plataforma Inteligente de Aprendizaje Basado en Preguntas",
                "version": "2.0.0",
            },
            "host": os.getenv("SWAGGER_HOST", "localhost:5000"),
            "basePath": "/api",
            "schemes": ["http", "https"],
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Token Firebase: Bearer <token>"
                }
            },
        })

    app.register_blueprint(auth_router)
    app.register_blueprint(course_router)
    app.register_blueprint(question_router)
    app.register_blueprint(ai_router)
    app.register_blueprint(progress_router)

    limiter.limit("30 per minute")(question_router)
    limiter.limit("30 per minute")(ai_router)
    limiter.limit("10 per minute")(auth_router)
    limiter.limit("60 per minute")(course_router)

    # === MANEJADORES GLOBALES DE ERRORES ===
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        """Captura errores de JSON malformado y retorna 400 en lugar de 500."""
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "El cuerpo de la solicitud no contiene un JSON valido o esta malformado."
        }), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        """Retorna JSON en lugar de HTML para 404."""
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "El recurso solicitado no existe."
        }), 404

    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        """Retorna JSON en lugar de HTML para errores 500 no manejados."""
        if isinstance(e, HTTPException) and e.code < 500:
            return jsonify({"success": False, "error": str(e)}), e.code
        logger.error("Error no manejado: %s", e, exc_info=True)
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "Ocurrio un error inesperado en el servidor."
        }), 500

    @app.route("/")
    def health():
        """Health check basico.
        ---
        tags:
          - Sistema
        responses:
          200:
            description: Servidor funcionando
        """
        return {
            "success": True,
            "message": "PreguntaIA backend funcionando",
            "version": "2.0.0",
        }

    @app.route("/health")
    def health_check():
        now = datetime.now(timezone.utc)
        return jsonify({
            "status":   "ok",
            "version":  "2.0.0",
            "timestamp": now.isoformat(),
        }), 200

    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app  = create_app()
    app.run(debug=debug, host="0.0.0.0", port=port)