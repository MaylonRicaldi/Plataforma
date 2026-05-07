from flask import Blueprint, jsonify, request
from datetime import datetime, timezone

from src.config.firebase_config import firebase_auth, db

router = Blueprint("auth", __name__, url_prefix="/api/auth")


# =========================================================
# REGISTER — crea en Auth + Firestore en un solo paso
# =========================================================
@router.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Datos no enviados"}), 400

    email    = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "message": "Email y password requeridos"}), 400

    try:
        # 1. Crear en Firebase Authentication
        auth_user = firebase_auth.create_user(
            email=email,
            password=password
        )

        uid = auth_user.uid
        now = datetime.now(timezone.utc)

        # 2. Guardar en Firestore — colección users, doc ID = uid
        user_data = {
            "uid":       uid,
            "email":     email,
            "name":      email,   # nombre = correo
            "role":      "student",
            "createdAt": now,
            "updatedAt": now
        }

        db.collection("users").document(uid).set(user_data)

        print(f"✅ Usuario guardado en Firestore: {uid}")

        return jsonify({
            "success": True,
            "message": "Usuario creado",
            "uid":     uid,
            "email":   email
        }), 201

    except Exception as e:
        print("REGISTER ERROR:", str(e))
        return jsonify({"success": False, "error": str(e)}), 400


# =========================================================
# ME — valida token y retorna/crea usuario en Firestore
# =========================================================
@router.route("/me", methods=["GET"])
def auth_me():

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    if not token:
        return jsonify({"success": False, "message": "Token no enviado"}), 401

    try:
        decoded = firebase_auth.verify_id_token(
            token,
            check_revoked=False,
            clock_skew_seconds=10
        )

        uid   = decoded["uid"]
        email = decoded.get("email", "")

        user_ref = db.collection("users").document(uid)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
        else:
            # Si por alguna razón no existe, lo crea
            now = datetime.now(timezone.utc)
            user_data = {
                "uid":       uid,
                "email":     email,
                "name":      email,
                "role":      "student",
                "createdAt": now,
                "updatedAt": now
            }
            user_ref.set(user_data)

        return jsonify({"success": True, "user": user_data}), 200

    except Exception as e:
        print("AUTH ME ERROR:", str(e))
        return jsonify({"success": False, "error": str(e)}), 401