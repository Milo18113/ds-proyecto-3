from pathlib import Path

from dotenv import load_dotenv

# Cargar .env de la raíz del repo antes de leer JWT, DATABASE_URL o CORS.
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.seed_users import seed_users

from backend.api.routes.auth_routes import router as auth_router
from backend.api.routes.incident_routes import router as incident_router
from backend.api.routes.task_routes import router as task_router
from backend.api.routes.notification_routes import router as notification_router
from backend.api.routes.user_routes import router as user_router

app = FastAPI(
    title="OpsCenter API",
    version="1.0.0",
    description="API del sistema OpsCenter",
)

def _cors_allow_origins() -> list[str]:
    """
    Orígenes permitidos para CORS (navegador). Lista separada por comas en CORS_ORIGINS.
    Por defecto solo Streamlit local; nunca usar '*' junto con allow_credentials=True.
    """
    raw = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    )
    return [o.strip() for o in raw.split(",") if o.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allow_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    seed_users()


@app.get("/")
def root():
    return {"message": "OpsCenter API running"}


app.include_router(auth_router)
app.include_router(incident_router)
app.include_router(task_router)
app.include_router(notification_router)
app.include_router(user_router)
