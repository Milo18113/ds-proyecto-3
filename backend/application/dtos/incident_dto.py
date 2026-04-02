from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from backend.domain.enums.severity import Severity
from backend.domain.enums.incident_status import IncidentStatus


# ── DTOs de entrada ───────────────────────────────────────────────────────

class CreateIncidentDTO(BaseModel):
    """DTO para la creación de un incidente."""
    title: str = Field(..., min_length=1, description="Título del incidente")
    description: str = Field(..., min_length=1, description="Descripción del incidente")
    severity: Severity = Field(..., description="Severidad: LOW, MEDIUM, HIGH, CRITICAL")


class AssignIncidentDTO(BaseModel):
    """DTO para asignar un incidente a un usuario."""
    assigned_to: str = Field(..., min_length=1, description="ID del usuario asignado")


class ChangeIncidentStatusDTO(BaseModel):
    """DTO para cambiar el estado de un incidente."""
    status: IncidentStatus = Field(..., description="Nuevo estado del incidente")


# ── DTOs de salida ────────────────────────────────────────────────────────

class IncidentResponseDTO(BaseModel):
    """DTO de respuesta para un incidente."""
    id: str
    title: str
    description: str
    severity: Severity
    status: IncidentStatus
    created_by: str
    assigned_to: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class IncidentDetailDTO(IncidentResponseDTO):
    """DTO de respuesta con detalle completo de un incidente (incluye tareas)."""
    tasks: list["TaskResponseDTO"] = []


# Importación diferida para evitar ciclo
from backend.application.dtos.task_dto import TaskResponseDTO  # noqa: E402

IncidentDetailDTO.model_rebuild()
