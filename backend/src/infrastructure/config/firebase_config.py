import os
import logging
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore, auth

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)   # sube hasta backend/
        )
    )
)

# Intentar FIREBASE_SERVICE_ACCOUNT_JSON (JSON string) primero,
# luego GOOGLE_APPLICATION_CREDENTIALS (path a archivo),
# fallback a path hardcodeado
firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
if firebase_json:
    import json
    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    logger.info("Firebase inicializado desde variable de entorno FIREBASE_SERVICE_ACCOUNT_JSON")
else:
    SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.path.join(BASE_DIR, "serviceAccountKey.json")
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    logger.info("Firebase inicializado desde: %s", SERVICE_ACCOUNT_PATH)

# Iniciar Firebase una sola vez
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Clientes globales
db            = firestore.client()
firebase_auth = auth
