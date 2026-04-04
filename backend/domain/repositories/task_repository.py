from abc import ABC, abstractmethod
from typing import Optional
from backend.domain.entities.task import Task


class TaskRepository(ABC):
    """Puerto de salida para persistencia de tareas."""

    @abstractmethod
    def save(self, task: Task) -> Task:
        ...

    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        ...

    @abstractmethod
    def find_all(self) -> list[Task]:
        ...

    @abstractmethod
    def find_by_assigned(self, user_id: str) -> list[Task]:
        ...

    @abstractmethod
    def find_by_incident(self, incident_id: str) -> list[Task]:
        ...

    @abstractmethod
    def update(self, task: Task) -> Task:
        ...
