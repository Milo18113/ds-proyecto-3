from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from datetime import datetime

from backend.infrastructure.orm.base import Base
from backend.domain.enums.task_status import TaskStatus


class TaskModel(Base):
    """Modelo ORM para la tabla tasks."""
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(
        SAEnum(TaskStatus, name="task_status_enum", create_constraint=True),
        nullable=False,
        default=TaskStatus.OPEN,
    )
    assigned_to = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
