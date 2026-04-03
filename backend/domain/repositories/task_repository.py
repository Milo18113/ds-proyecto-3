from abc import ABC, abstractmethod
from backend.domain.entities.task import Task


class TaskRepository(ABC):
    """
    Puerto de salida para persistencia de tareas.
    La implementación concreta vive en infrastructure/repositories/.
    """

    @abstractmethod
    def save(self, task: Task) -> None:
        """Persiste una tarea nueva o actualiza una existente."""
        ...

    @abstractmethod
    def find_by_id(self, task_id: str) -> Task | None:
        """Retorna una tarea por su ID, o None si no existe."""
        ...

    @abstractmethod
    def find_all(self) -> list[Task]:
        """Retorna todas las tareas. Usado por Admin."""
        ...

    @abstractmethod
    def find_by_incident_id(self, incident_id: str) -> list[Task]:
        """Retorna todas las tareas asociadas a un incidente."""
        ...

    @abstractmethod
    def find_by_assigned_to(self, user_id: str) -> list[Task]:
        """Retorna tareas asignadas a un usuario específico.
        Usado para la vista del Operator."""
        ...

    @abstractmethod
    def delete(self, task_id: str) -> None:
        """Elimina una tarea por su ID."""
        ...