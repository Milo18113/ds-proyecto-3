from backend.domain.states.incident_state import IncidentState, InvalidTransitionError
from backend.domain.enums.incident_status import IncidentStatus


class InProgressState(IncidentState):
    """
    El incidente está siendo trabajado activamente.
    Solo permite transicionar a RESOLVED.
    """

    def assign(self, incident) -> None:
        # Permitido: reasignar mientras está en progreso
        pass

    def start_progress(self, incident) -> None:
        self._invalid_transition(IncidentStatus.IN_PROGRESS)

    def resolve(self, incident) -> None:
        from backend.domain.states.resolved_state import ResolvedState
        incident.status = IncidentStatus.RESOLVED
        incident.state = ResolvedState()

    def close(self, incident) -> None:
        self._invalid_transition(IncidentStatus.CLOSED)

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.IN_PROGRESS