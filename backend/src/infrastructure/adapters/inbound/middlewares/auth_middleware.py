import logging
from functools import wraps

from flask import request, jsonify, g

from src.infrastructure.config.firebase_config import firebase_auth

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")


def require_auth(f):
    """
    Decorador que valida el token Firebase en el header Authorization.
    Inyecta g.uid y g.email en el contexto de la solicitud.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token       = auth_header.replace("Bearer ", "").strip()
        endpoint    = request.endpoint or "unknown"

        if not token:
            security_logger.warning("EVENTO=TOKEN_FALTANTE endpoint=%s ip=%s", endpoint, request.remote_addr)
            return jsonify({
                "success": False,
                "message": "Token de autenticación no enviado",
            }), 401

        try:
            decoded  = firebase_auth.verify_id_token(
                token,
                check_revoked=True,
                clock_skew_seconds=10,
            )
            g.uid   = decoded["uid"]
            g.email = decoded.get("email", "")
            logger.info("Auth exitoso: uid=%s endpoint=%s", g.uid, endpoint)
        except Exception as e:
            g.uid = None
            g.email = None
            error_str = str(e)
            if "expired" in error_str.lower():
                security_logger.warning("EVENTO=TOKEN_EXPIRADO endpoint=%s ip=%s", endpoint, request.remote_addr)
                return jsonify({
                    "success": False,
                    "message": "Token expirado",
                }), 401
            security_logger.warning("EVENTO=TOKEN_INVALIDO endpoint=%s ip=%s error=%s", endpoint, request.remote_addr, error_str)
            return jsonify({
                "success": False,
                "message": "Token inválido o expirado",
            }), 401

        return f(*args, **kwargs)

    return decorated
