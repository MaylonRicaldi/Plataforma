import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore, auth

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)   # sube hasta backend/
        )
    )
)

SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

# Iniciar Firebase una sola vez
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

# Clientes globales
db            = firestore.client()
firebase_auth = auth
