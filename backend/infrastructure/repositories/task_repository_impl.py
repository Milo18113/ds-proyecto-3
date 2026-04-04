from typing import Optional
from sqlalchemy.orm import Session

from backend.domain.entities.task import Task
from backend.domain.repositories.task_repository import TaskRepository
from backend.infrastructure.orm.models.task_model import TaskModel


class TaskRepositoryImpl(TaskRepository):
    """Implementación concreta del repositorio de tareas usando SQLAlchemy ORM."""

    def __init__(self, db: Session):
        self.db = db

    # ── Mappers ───────────────────────────────────────────────────────────

    def _to_domain(self, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            incident_id=model.incident_id,
            title=model.title,
            description=model.description,
            assigned_to=model.assigned_to,
            created_at=model.created_at,
            status=model.status,
        )

    def _to_model(self, entity: Task) -> TaskModel:
        return TaskModel(
            id=entity.id,
            incident_id=entity.incident_id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            assigned_to=entity.assigned_to,
            created_at=entity.created_at,
        )

    # ── CRUD ──────────────────────────────────────────────────────────────

    def save(self, task: Task) -> Task:
        model = self._to_model(task)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def find_by_id(self, task_id: str) -> Optional[Task]:
        model = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self._to_domain(model) if model else None

    def find_all(self) -> list[Task]:
        models = self.db.query(TaskModel).order_by(TaskModel.created_at.desc()).all()
        return [self._to_domain(m) for m in models]

    def find_by_assigned(self, user_id: str) -> list[Task]:
        models = (
            self.db.query(TaskModel)
            .filter(TaskModel.assigned_to == user_id)
            .order_by(TaskModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def find_by_incident(self, incident_id: str) -> list[Task]:
        models = (
            self.db.query(TaskModel)
            .filter(TaskModel.incident_id == incident_id)
            .order_by(TaskModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def update(self, task: Task) -> Task:
        model = self.db.query(TaskModel).filter(TaskModel.id == task.id).first()
        if not model:
            raise ValueError(f"Tarea {task.id} no encontrada.")
        model.title = task.title
        model.description = task.description
        model.status = task.status
        model.assigned_to = task.assigned_to
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
