from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.factories.entity_factory import IncidentFactory
from backend.infrastructure.events.event_bus import EventBus
from backend.application.dtos.incident_dto import CreateIncidentDTO, IncidentResponseDTO
from backend.domain.events.event import Event
from backend.domain.enums.event_type import EventType


class CreateIncidentUseCase:
    def __init__(
        self,
        incident_repo: IncidentRepository,
        event_bus: EventBus,
    ):
        self.incident_repo = incident_repo
        self.event_bus = event_bus

    def execute(self, dto: CreateIncidentDTO, created_by: str) -> IncidentResponseDTO:
        incident = IncidentFactory.create(
            title=dto.title,
            description=dto.description,
            severity=dto.severity,
            created_by=created_by,
        )

        saved = self.incident_repo.save(incident)

        event = Event(
            event_type=EventType.INCIDENT_CREATED,
            payload={
                "incident_id": saved.id,
                "title": saved.title,
                "description": saved.description,
                "severity": saved.severity,
                "status": saved.status,
                "created_by": saved.created_by,
                "assigned_to": saved.assigned_to,
            },
        )
        self.event_bus.publish(event)

        return IncidentResponseDTO(
            id=saved.id,
            title=saved.title,
            description=saved.description,
            severity=saved.severity,
            status=saved.status,
            created_by=saved.created_by,
            assigned_to=saved.assigned_to,
            created_at=saved.created_at,
        )