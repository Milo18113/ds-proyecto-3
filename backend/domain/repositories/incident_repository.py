from abc import ABC, abstractmethod
from backend.domain.entities.incident import Incident


class IncidentRepository(ABC):
    """
    Puerto de salida para persistencia de incidentes.
    La implementación concreta vive en infrastructure/repositories/.
    """

    @abstractmethod
    def save(self, incident: Incident) -> None:
        """Persiste un incidente nuevo o actualiza uno existente."""
        ...

    @abstractmethod
    def find_by_id(self, incident_id: str) -> Incident | None:
        """Retorna un incidente por su ID, o None si no existe."""
        ...

    @abstractmethod
    def find_all(self) -> list[Incident]:
        """Retorna todos los incidentes. Usado por Admin y Supervisor."""
        ...

    @abstractmethod
    def find_by_created_by(self, user_id: str) -> list[Incident]:
        """Retorna incidentes creados por un usuario específico."""
        ...

    @abstractmethod
    def find_by_assigned_to(self, user_id: str) -> list[Incident]:
        """Retorna incidentes asignados a un usuario específico."""
        ...

    @abstractmethod
    def find_by_created_by_or_assigned_to(self, user_id: str) -> list[Incident]:
        """Retorna incidentes donde el usuario es creador o asignado.
        Usado para la vista del Operator."""
        ...

    @abstractmethod
    def delete(self, incident_id: str) -> None:
        """Elimina un incidente por su ID."""
        ...