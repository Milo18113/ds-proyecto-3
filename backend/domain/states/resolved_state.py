from backend.domain.states.incident_state import IncidentState, InvalidTransitionError
from backend.domain.enums.incident_status import IncidentStatus


class ResolvedState(IncidentState):
    """
    El incidente fue resuelto.
    Solo permite transicionar a CLOSED.
    """

    def assign(self, incident) -> None:
        self._invalid_transition(IncidentStatus.ASSIGNED)

    def start_progress(self, incident) -> None:
        self._invalid_transition(IncidentStatus.IN_PROGRESS)

    def resolve(self, incident) -> None:
        self._invalid_transition(IncidentStatus.RESOLVED)

    def close(self, incident) -> None:
        from backend.domain.states.closed_state import ClosedState
        incident.status = IncidentStatus.CLOSED
        incident.state = ClosedState()

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.RESOLVED