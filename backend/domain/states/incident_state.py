from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from backend.domain.enums.incident_status import IncidentStatus

if TYPE_CHECKING:
    from backend.domain.entities.incident import Incident


class IncidentState(ABC):
    """
    Estado abstracto del ciclo de vida de un incidente.
    Cada estado concreto define qué transiciones están permitidas
    y cuáles deben rechazar con InvalidTransitionError.
    """

    @abstractmethod
    def assign(self, incident: Incident) -> None:
        """Transición hacia ASSIGNED."""
        ...

    @abstractmethod
    def start_progress(self, incident: Incident) -> None:
        """Transición hacia IN_PROGRESS."""
        ...

    @abstractmethod
    def resolve(self, incident: Incident) -> None:
        """Transición hacia RESOLVED."""
        ...

    @abstractmethod
    def close(self, incident: Incident) -> None:
        """Transición hacia CLOSED."""
        ...

    @abstractmethod
    def get_status(self) -> IncidentStatus:
        """Retorna el enum del estado concreto."""
        ...

    def _invalid_transition(self, target: IncidentStatus) -> None:
        """
        Lanza excepción con mensaje claro para transiciones no permitidas.
        """
        raise InvalidTransitionError(
            f"No se puede pasar de {self.get_status().value} a {target.value}."
        )


class InvalidTransitionError(Exception):
    """
    Excepción de dominio para transiciones de estado inválidas.
    No hereda de HTTPException — eso lo maneja la capa API.
    """
    pass