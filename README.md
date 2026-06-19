# PlataformaLIA (PreguntaIA)

Plataforma educativa inteligente de aprendizaje basado en preguntas. Permite a estudiantes crear preguntas, recibir retroalimentación con IA (Taxonomía de Bloom + Gemini) y dar seguimiento a su progreso cognitivo.

## Stack

- **Backend:** Python 3.12 + Flask (Clean Architecture / Hexagonal)
- **Frontend:** React 19 + Vite 8 (JSX)
- **Base de datos:** Firebase Firestore
- **Autenticación:** Firebase Authentication
- **IA:** Google Gemini 2.5 Flash + motor local de Taxonomía de Bloom
- **Testing:** pytest, Cypress, Selenium, MLflow

## Estructura del proyecto

```
backend/src/               # Código fuente backend
  application/             # Casos de uso y servicios
  domain/                  # Entidades y puertos (interfaces)
  infrastructure/          # Adaptadores (controladores, DB, AI)
  config/                  # Configuración (Firebase)
  main.py                  # Punto de entrada Flask

frontend/src/              # Código fuente frontend
  pages/                   # Componentes de página
  services/                # Cliente API (Axios)
  app/                     # Configuración Firebase

tests/                     # Pruebas
  backend/                 # pytest (unitarias + integración)
  selenium/                # Pruebas de interfaz
  cypress/                 # Pruebas E2E
  ml/                      # Evaluación del motor Bloom
  postman/                 # Colección de API
```

## Requisitos

- Python 3.12+
- Node.js 20+
- Firebase project con Firestore y Authentication habilitados
- API key de Google Gemini (opcional — el motor Bloom local funciona sin ella)

## Configuración

### Backend

```bash
cd backend
cp .env.example .env
# Editar .env con:
# - GEMINI_API_KEY: tu clave de Gemini (o dejar vacío para usar solo Bloom local)
# - GOOGLE_APPLICATION_CREDENTIALS: ruta a serviceAccountKey.json de Firebase

python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt

python src/main.py
# Servidor en http://localhost:5000
```

### Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
# Servidor en http://localhost:5173
```

### Variables de entorno

Ver `.env.example` en `backend/` y `frontend/` para la lista completa.

## APIs

### Endpoints principales

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | /api/auth/register | No | Registrar usuario |
| GET | /api/auth/me | Sí | Perfil del usuario actual |
| GET | /api/courses | Sí | Listar cursos |
| GET | /api/courses/:id/questions | Sí | Preguntas por curso |
| POST | /api/questions | Sí | Crear pregunta (con IA) |
| GET | /api/questions/:id | No | Detalle de pregunta |
| PUT | /api/questions/:id | Sí | Editar pregunta |
| DELETE | /api/questions/:id | Sí | Eliminar pregunta |
| POST | /api/ai/improve-question | Sí | Previsualizar mejora IA |
| GET | /api/progress | Sí | Progreso del usuario |
| GET | /health | No | Health check |

## Pruebas

```bash
# Backend (pytest)
cd tests/backend
pytest -v

# Frontend (Cypress E2E)
cd frontend
npx cypress run

# Cobertura
pytest --cov=src tests/backend/
```

## Arquitectura

El backend sigue una arquitectura hexagonal (puertos y adaptadores):

- **Controladores** (inbound adapters): manejan requests HTTP
- **Casos de uso** (application): contienen la lógica de negocio
- **Puertos** (domain): interfaces para repositorios y servicios externos
- **Adaptadores** (outbound): implementan los puertos (Firestore, Gemini, etc.)
