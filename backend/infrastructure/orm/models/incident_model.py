from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from datetime import datetime

from backend.infrastructure.orm.base import Base
from backend.domain.enums.severity import Severity
from backend.domain.enums.incident_status import IncidentStatus


class IncidentModel(Base):
    """Modelo ORM para la tabla incidents."""
    __tablename__ = "incidents"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    severity = Column(
        SAEnum(Severity, name="severity_enum", create_constraint=True),
        nullable=False,
    )
    status = Column(
        SAEnum(IncidentStatus, name="incident_status_enum", create_constraint=True),
        nullable=False,
        default=IncidentStatus.OPEN,
    )
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
