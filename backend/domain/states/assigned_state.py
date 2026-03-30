from backend.domain.states.incident_state import IncidentState, InvalidTransitionError
from backend.domain.enums.incident_status import IncidentStatus


class AssignedState(IncidentState):
    """
    El incidente tiene un responsable asignado.
    Solo permite transicionar a IN_PROGRESS.
    """

    def assign(self, incident) -> None:
        # Permitido: reasignar sin cambiar de estado
        pass

    def start_progress(self, incident) -> None:
        from backend.domain.states.in_progress_state import InProgressState
        incident.status = IncidentStatus.IN_PROGRESS
        incident.state = InProgressState()

    def resolve(self, incident) -> None:
        self._invalid_transition(IncidentStatus.RESOLVED)

    def close(self, incident) -> None:
        self._invalid_transition(IncidentStatus.CLOSED)

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.ASSIGNED