from pydantic import BaseModel, Field
from datetime import datetime

from backend.domain.enums.task_status import TaskStatus


# ── DTOs de entrada ───────────────────────────────────────────────────────

class CreateTaskDTO(BaseModel):
    """DTO para la creación de una tarea asociada a un incidente."""
    incident_id: str = Field(..., min_length=1, description="ID del incidente padre")
    title: str = Field(..., min_length=1, description="Título de la tarea")
    description: str = Field(..., min_length=1, description="Descripción de la tarea")
    assigned_to: str = Field(..., min_length=1, description="ID del usuario responsable")


class ChangeTaskStatusDTO(BaseModel):
    """DTO para cambiar el estado de una tarea."""
    status: TaskStatus = Field(..., description="Nuevo estado: OPEN, IN_PROGRESS, DONE")


# ── DTOs de salida ────────────────────────────────────────────────────────

class TaskResponseDTO(BaseModel):
    """DTO de respuesta para una tarea."""
    id: str
    incident_id: str
    title: str
    description: str
    status: TaskStatus
    assigned_to: str
    created_at: datetime

    class Config:
        from_attributes = True
