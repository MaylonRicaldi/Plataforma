import logging
import re
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, g

from src.infrastructure.config.firebase_config import firebase_auth, db
from src.infrastructure.adapters.inbound.middlewares.auth_middleware import require_auth

logger = logging.getLogger(__name__)
router = Blueprint("auth", __name__, url_prefix="/api/auth")


# ══════════════════════════════════════════════════════
# REGISTER  — HU-23, HU-24
# ══════════════════════════════════════════════════════
@router.route("/register", methods=["POST"])
def register():
    """Registrar un nuevo usuario.
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuario creado exitosamente
      400:
        description: Error de validacion
      409:
        description: Email ya registrado
    """
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"success": False, "message": "Datos no enviados"}), 400

    email    = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "message": "Email y password requeridos"}), 400

    if len(password) < 8:
        return jsonify({"success": False, "message": "La contraseña debe tener al menos 8 caracteres"}), 400
    if not re.search(r"[A-Z]", password):
        return jsonify({"success": False, "message": "La contraseña debe contener al menos una mayúscula"}), 400
    if not re.search(r"\d", password):
        return jsonify({"success": False, "message": "La contraseña debe contener al menos un número"}), 400

    try:
        masked = email[:3] + "***" if email else "***"
        logger.info("Registrando nuevo usuario: %s", masked)
        auth_user = firebase_auth.create_user(email=email, password=password)
        uid       = auth_user.uid
        now       = datetime.now(timezone.utc)

        user_data = {
            "uid":       uid,
            "email":     email,
            "name":      email,
            "role":      "student",
            "createdAt": now,
            "updatedAt": now,
        }

        try:
            db.collection("users").document(uid).set(user_data)
        except Exception as firestore_err:
            logger.error("Error creando perfil en Firestore para %s, revirtiendo Auth user: %s", uid, firestore_err)
            firebase_auth.delete_user(uid)
            return jsonify({
                "success": False,
                "message": "Error al crear el perfil de usuario. Intenta de nuevo."
            }), 500

        return jsonify({
            "success": True,
            "message": "Usuario creado correctamente",
            "uid":     uid,
            "email":   email,
        }), 201

    except Exception as e:
        error_str = str(e)
        if "EMAIL_EXISTS" in error_str or "email-already-exists" in error_str:
            logger.warning("Registro fallido: email ya existe - %s", email)
            return jsonify({"success": False, "message": "Este correo ya está registrado"}), 409
        logger.error("Registro fallido: %s", error_str)
        return jsonify({"success": False, "message": "Error al crear usuario", "error": error_str}), 400


# ══════════════════════════════════════════════════════
# ME  — HU-23, HU-24
# ══════════════════════════════════════════════════════
@router.route("/me", methods=["GET"])
@require_auth
def auth_me():
    """Obtener perfil del usuario autenticado.
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Datos del usuario
      401:
        description: Token invalido o no enviado
    """
    uid   = g.uid
    email = g.email

    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data      = user_doc.to_dict()
        user_data["id"] = uid
    else:
        logger.info("Usuario no existia en Firestore, creando perfil para %s", email)
        now = datetime.now(timezone.utc)
        user_data = {
            "uid":       uid,
            "email":     email,
            "name":      email,
            "role":      "student",
            "createdAt": now,
            "updatedAt": now,
        }
        user_ref.set(user_data)
        user_data["id"] = uid

    return jsonify({"success": True, "user": user_data}), 200
