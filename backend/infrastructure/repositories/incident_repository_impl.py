from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.domain.entities.incident import Incident
from backend.domain.repositories.incident_repository import IncidentRepository
from backend.domain.enums.severity import Severity
from backend.domain.enums.incident_status import IncidentStatus
from backend.infrastructure.orm.models.incident_model import IncidentModel


class IncidentRepositoryImpl(IncidentRepository):
    """Implementación concreta del repositorio de incidentes usando SQLAlchemy ORM."""

    def __init__(self, db: Session):
        self.db = db

    # ── Mappers ───────────────────────────────────────────────────────────

    def _to_domain(self, model: IncidentModel) -> Incident:
        """Convierte un modelo ORM a entidad de dominio."""
        incident = Incident(
            id=model.id,
            title=model.title,
            description=model.description,
            severity=model.severity,
            created_by=model.created_by,
            created_at=model.created_at,
            status=model.status,
            assigned_to=model.assigned_to,
        )
        # Restaurar el state correcto según el status persistido
        incident.state = self._resolve_state(model.status)
        incident.status = model.status
        return incident

    def _to_model(self, entity: Incident) -> IncidentModel:
        """Convierte una entidad de dominio a modelo ORM."""
        return IncidentModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            severity=entity.severity,
            status=entity.status,
            created_by=entity.created_by,
            assigned_to=entity.assigned_to,
            created_at=entity.created_at,
        )

    @staticmethod
    def _resolve_state(status: IncidentStatus):
        """Retorna la instancia de State correcta según el status almacenado."""
        from backend.domain.states.open_state import OpenState
        from backend.domain.states.assigned_state import AssignedState
        from backend.domain.states.in_progress_state import InProgressState
        from backend.domain.states.resolved_state import ResolvedState
        from backend.domain.states.closed_state import ClosedState

        mapping = {
            IncidentStatus.OPEN: OpenState,
            IncidentStatus.ASSIGNED: AssignedState,
            IncidentStatus.IN_PROGRESS: InProgressState,
            IncidentStatus.RESOLVED: ResolvedState,
            IncidentStatus.CLOSED: ClosedState,
        }
        return mapping[status]()

    # ── CRUD ──────────────────────────────────────────────────────────────

    def save(self, incident: Incident) -> Incident:
        model = self._to_model(incident)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def find_by_id(self, incident_id: str) -> Optional[Incident]:
        model = self.db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
        return self._to_domain(model) if model else None

    def find_all(self) -> list[Incident]:
        models = self.db.query(IncidentModel).order_by(IncidentModel.created_at.desc()).all()
        return [self._to_domain(m) for m in models]

    def find_by_creator(self, user_id: str) -> list[Incident]:
        models = (
            self.db.query(IncidentModel)
            .filter(IncidentModel.created_by == user_id)
            .order_by(IncidentModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def find_by_assigned(self, user_id: str) -> list[Incident]:
        models = (
            self.db.query(IncidentModel)
            .filter(IncidentModel.assigned_to == user_id)
            .order_by(IncidentModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def find_by_creator_or_assigned(self, user_id: str) -> list[Incident]:
        models = (
            self.db.query(IncidentModel)
            .filter(
                or_(
                    IncidentModel.created_by == user_id,
                    IncidentModel.assigned_to == user_id,
                )
            )
            .order_by(IncidentModel.created_at.desc())
            .all()
        )
        return [self._to_domain(m) for m in models]

    def update(self, incident: Incident) -> Incident:
        model = self.db.query(IncidentModel).filter(IncidentModel.id == incident.id).first()
        if not model:
            raise ValueError(f"Incidente {incident.id} no encontrado.")
        model.title = incident.title
        model.description = incident.description
        model.severity = incident.severity
        model.status = incident.status
        model.assigned_to = incident.assigned_to
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
