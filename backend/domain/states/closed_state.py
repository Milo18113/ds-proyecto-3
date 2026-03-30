from backend.domain.states.incident_state import IncidentState, InvalidTransitionError
from backend.domain.enums.incident_status import IncidentStatus


class ClosedState(IncidentState):
    """
    Estado terminal. Un incidente cerrado no puede cambiar de estado.
    Ninguna transición está permitida.
    """

    def assign(self, incident) -> None:
        self._invalid_transition(IncidentStatus.ASSIGNED)

    def start_progress(self, incident) -> None:
        self._invalid_transition(IncidentStatus.IN_PROGRESS)

    def resolve(self, incident) -> None:
        self._invalid_transition(IncidentStatus.RESOLVED)

    def close(self, incident) -> None:
        self._invalid_transition(IncidentStatus.CLOSED)

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.CLOSED