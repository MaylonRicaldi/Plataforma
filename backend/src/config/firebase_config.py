import os
from dotenv import load_dotenv

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


# cargar .env
load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


SERVICE_ACCOUNT_PATH = os.path.join(
    BASE_DIR,
    "serviceAccountKey.json"
)


# iniciar Firebase una sola vez
if not firebase_admin._apps:

    cred = credentials.Certificate(
        SERVICE_ACCOUNT_PATH
    )

    firebase_admin.initialize_app(
        cred
    )


# clientes globales
db = firestore.client()

firebase_auth = auth
