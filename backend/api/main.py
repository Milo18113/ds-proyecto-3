from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.infrastructure.database.connection import init_db
from backend.api.routes.auth_routes import router as auth_router
from backend.api.routes.incident_routes import router as incident_router
from backend.api.routes.task_routes import router as task_router
from backend.api.routes.notification_routes import router as notification_router

app = FastAPI(
    title="OpsCenter API",
    version="1.0.0",
    description="API del sistema OpsCenter",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "OpsCenter API running"}


app.include_router(auth_router)
app.include_router(incident_router)
app.include_router(task_router)
app.include_router(notification_router)