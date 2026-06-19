# PlataformaLIA (PreguntaIA)

Plataforma educativa inteligente de aprendizaje basado en preguntas. Permite a estudiantes crear preguntas, recibir retroalimentación con IA (Taxonomía de Bloom + Gemini) y dar seguimiento a su progreso cognitivo.

## Stack

* **Backend:** Python 3.12 + Flask (Arquitectura Hexagonal)
* **Frontend:** React 19 + Vite 8 (JSX)
* **Base de datos:** Firebase Firestore
* **Autenticación:** Firebase Authentication
* **IA:** Google Gemini 2.5 Flash + motor local de Taxonomía de Bloom
* **Testing:** pytest
* **CI/CD:** GitHub Actions

## Estructura del proyecto

```text
backend/
├── logs/                          # Logs de la aplicación
├── mlflow.db                      # Base de datos MLflow
├── requirements.txt               # Dependencias Python
└── src/
    ├── application/               # Casos de uso y servicios
    │   ├── services/              # Servicios de aplicación
    │   └── use_cases/             # Casos de uso
    ├── config/                    # Configuración
    ├── domain/                    # Capa de dominio
    │   ├── entities/              # Entidades
    │   ├── enums/                 # Enumeraciones
    │   └── ports/                 # Interfaces (puertos)
    ├── infrastructure/            # Adaptadores
    │   ├── adapters/
    │   │   ├── inbound/           # Controladores HTTP
    │   │   └── outbound/          # Firestore, Gemini, etc.
    │   └── config/                # Configuración Firebase
    ├── routes/                    # Definición de rutas
    └── main.py                    # Punto de entrada Flask

frontend/
├── public/                        # Archivos estáticos
└── src/
    ├── app/                       # Configuración Firebase
    ├── assets/                    # Recursos estáticos
    ├── pages/                     # Componentes de página
    ├── services/                  # Cliente API (Axios)
    ├── App.jsx                    # Componente principal
    ├── ErrorBoundary.jsx          # Manejo de errores
    ├── Layout.jsx                 # Layout principal
    ├── Spinner.jsx                # Indicador de carga
    ├── ToastContext.jsx           # Notificaciones
    ├── index.css                  # Estilos globales
    └── main.jsx                   # Punto de entrada React

.github/
└── workflows/
    └── ci.yml                     # Pipeline CI/CD
```

## Requisitos

* **Python:** 3.12+
* **Node.js:** 20+
* **Firebase:** Firestore y Authentication habilitados.
* **Google Gemini API Key:** Opcional (el motor Bloom local funciona sin ella).

## Configuración

### Backend

```bash
cd backend

cp .env.example .env

# Configurar:
# GEMINI_API_KEY=tu_clave_de_gemini
# GOOGLE_APPLICATION_CREDENTIALS=ruta/serviceAccountKey.json

python -m venv venv

# Windows
.\venv\Scripts\activate

pip install -r requirements.txt

python src/main.py
```

Servidor:

```text
http://localhost:5000
```

### Frontend

```bash
cd frontend

cp .env.example .env

npm install

npm run dev
```

Servidor:

```text
http://localhost:5173
```

## Variables de entorno

Consultar los archivos:

* `backend/.env.example`
* `frontend/.env.example`

## API REST

### Endpoints principales

| Método | Ruta                         | Auth | Descripción                 |
| ------ | ---------------------------- | ---- | --------------------------- |
| POST   | `/api/auth/register`         | No   | Registrar usuario           |
| GET    | `/api/auth/me`               | Sí   | Perfil del usuario actual   |
| GET    | `/api/courses`               | Sí   | Listar cursos               |
| GET    | `/api/courses/:id/questions` | Sí   | Preguntas por curso         |
| POST   | `/api/questions`             | Sí   | Crear pregunta con IA       |
| GET    | `/api/questions/:id`         | No   | Obtener detalle de pregunta |
| PUT    | `/api/questions/:id`         | Sí   | Editar pregunta             |
| DELETE | `/api/questions/:id`         | Sí   | Eliminar pregunta           |
| POST   | `/api/ai/improve-question`   | Sí   | Previsualizar mejora con IA |
| GET    | `/api/progress`              | Sí   | Progreso del usuario        |
| GET    | `/health`                    | No   | Estado del servidor         |

## Pruebas

### Ejecutar pruebas backend

```bash
cd backend

pytest -v
```

### Cobertura

```bash
pytest --cov=src
```

## Arquitectura

El backend implementa una **Arquitectura Hexagonal (Ports & Adapters)**.

### Componentes principales

* **Controladores (Inbound Adapters):** reciben y procesan solicitudes HTTP.
* **Casos de uso (Application):** contienen la lógica de negocio.
* **Puertos (Domain):** definen interfaces para repositorios y servicios externos.
* **Adaptadores (Outbound Adapters):** implementan la comunicación con Firestore, Gemini y otros servicios.
