from backend.domain.states.incident_state import IncidentState, InvalidTransitionError
from backend.domain.enums.incident_status import IncidentStatus


class OpenState(IncidentState):
    """
    Estado inicial de todo incidente recién creado.
    Solo permite transicionar a ASSIGNED.
    """

    def assign(self, incident) -> None:
        from backend.domain.states.assigned_state import AssignedState
        incident.status = IncidentStatus.ASSIGNED
        incident.state = AssignedState()

    def start_progress(self, incident) -> None:
        self._invalid_transition(IncidentStatus.IN_PROGRESS)

    def resolve(self, incident) -> None:
        self._invalid_transition(IncidentStatus.RESOLVED)

    def close(self, incident) -> None:
        self._invalid_transition(IncidentStatus.CLOSED)

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.OPEN