from abc import ABC, abstractmethod
from backend.domain.enums.incident_status import IncidentStatus


class IncidentState(ABC):
    """
    Clase base abstracta del patrón State aplicado a Incident.
    Cada estado concreto define qué transiciones son válidas
    y cuáles deben lanzar excepción.
    """

    @abstractmethod
    def assign(self, incident: "Incident") -> None:
        """Transición hacia ASSIGNED."""
        ...

    @abstractmethod
    def start_progress(self, incident: "Incident") -> None:
        """Transición hacia IN_PROGRESS."""
        ...

    @abstractmethod
    def resolve(self, incident: "Incident") -> None:
        """Transición hacia RESOLVED."""
        ...

    @abstractmethod
    def close(self, incident: "Incident") -> None:
        """Transición hacia CLOSED."""
        ...

    @abstractmethod
    def get_status(self) -> IncidentStatus:
        """Retorna el IncidentStatus que representa este estado."""
        ...

    def _invalid_transition(self, target: IncidentStatus) -> None:
        """Lanza excepción con mensaje claro para transiciones no permitidas."""
        raise InvalidTransitionError(
            f"No se puede pasar de {self.get_status().value} a {target.value}."
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class InvalidTransitionError(Exception):
    """
    Excepción de dominio para transiciones de estado inválidas.
    No hereda de HTTPException — eso lo maneja la capa API.
    """
    pass


# Importación diferida para evitar ciclo de importación con Incident
from backend.domain.entities.incident import Incident  # noqa: E402