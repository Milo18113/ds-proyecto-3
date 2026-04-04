from abc import ABC, abstractmethod
from typing import Optional
from backend.domain.entities.incident import Incident


class IncidentRepository(ABC):
    """Puerto de salida para persistencia de incidentes."""

    @abstractmethod
    def save(self, incident: Incident) -> Incident:
        ...

    @abstractmethod
    def find_by_id(self, incident_id: str) -> Optional[Incident]:
        ...

    @abstractmethod
    def find_all(self) -> list[Incident]:
        ...

    @abstractmethod
    def find_by_creator(self, user_id: str) -> list[Incident]:
        ...

    @abstractmethod
    def find_by_assigned(self, user_id: str) -> list[Incident]:
        ...

    @abstractmethod
    def find_by_creator_or_assigned(self, user_id: str) -> list[Incident]:
        ...

    @abstractmethod
    def update(self, incident: Incident) -> Incident:
        ...
