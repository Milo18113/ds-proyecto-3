import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.infrastructure.orm.base import Base

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL no está definida. Configúrala en el entorno o en .env "
        "(ver .env.example). En Docker Compose suele apuntar al host `db`."
    )

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Session:
    """Generador de sesión para inyección de dependencias en FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea todas las tablas a partir de los modelos ORM registrados."""
    import backend.infrastructure.orm.models.user_model  # noqa: F401
    import backend.infrastructure.orm.models.incident_model  # noqa: F401
    import backend.infrastructure.orm.models.task_model  # noqa: F401
    import backend.infrastructure.orm.models.notification_model  # noqa: F401

    Base.metadata.create_all(bind=engine)