from uuid import uuid4
from datetime import datetime

from backend.domain.entities.incident import Incident
from backend.domain.entities.task import Task
from backend.domain.entities.notification import Notification
from backend.domain.enums.severity import Severity
from backend.domain.enums.event_type import EventType


class IncidentFactory:
    """
    Factory para crear entidades Incident de forma consistente.
    Centraliza la generación de IDs, timestamps y validaciones iniciales.
    """

    @staticmethod
    def create(
        title: str,
        description: str,
        severity: Severity,
        created_by: str,
    ) -> Incident:
        if not title or not title.strip():
            raise ValueError("El título del incidente no puede estar vacío.")
        if not description or not description.strip():
            raise ValueError("La descripción del incidente no puede estar vacía.")
        if not isinstance(severity, Severity):
            raise ValueError(f"Severidad inválida: {severity}")

        return Incident(
            id=str(uuid4()),
            title=title.strip(),
            description=description.strip(),
            severity=severity,
            created_by=created_by,
            created_at=datetime.utcnow(),
        )


class TaskFactory:
    """
    Factory para crear entidades Task de forma consistente.
    Centraliza la generación de IDs, timestamps y validaciones iniciales.
    """

    @staticmethod
    def create(
        incident_id: str,
        title: str,
        description: str,
        assigned_to: str,
    ) -> Task:
        if not title or not title.strip():
            raise ValueError("El título de la tarea no puede estar vacío.")
        if not description or not description.strip():
            raise ValueError("La descripción de la tarea no puede estar vacía.")
        if not incident_id or not incident_id.strip():
            raise ValueError("La tarea debe estar asociada a un incidente.")
        if not assigned_to or not assigned_to.strip():
            raise ValueError("La tarea debe tener un responsable asignado.")

        return Task(
            id=str(uuid4()),
            incident_id=incident_id.strip(),
            title=title.strip(),
            description=description.strip(),
            assigned_to=assigned_to.strip(),
            created_at=datetime.utcnow(),
        )


class NotificationFactory:
    """
    Factory para crear entidades Notification de forma consistente.
    """

    @staticmethod
    def create(
        recipient: str,
        channel: str,
        message: str,
        event_type: EventType,
    ) -> Notification:
        return Notification(
            id=str(uuid4()),
            recipient=recipient,
            channel=channel,
            message=message,
            event_type=event_type,
            created_at=datetime.utcnow(),
        )
