from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from backend.domain.enums.role import Role


@dataclass
class User:
    """
    Entidad de dominio base para todos los usuarios del sistema.
    No depende de ORM ni de ninguna capa de infraestructura.
    """
    id: str
    name: str
    email: str
    hashed_password: str
    role: Role
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())

    def can_view_all_incidents(self) -> bool:
        raise NotImplementedError

    def can_assign_incident(self) -> bool:
        raise NotImplementedError

    def can_change_incident_status(self) -> bool:
        raise NotImplementedError

    def can_view_all_tasks(self) -> bool:
        raise NotImplementedError

    def can_view_all_notifications(self) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} email={self.email}>"


@dataclass
class Operator(User):
    """
    Rol con permisos mínimos. Puede crear incidentes y ver
    únicamente los recursos que le pertenecen o están asignados a él.
    """
    role: Role = field(default=Role.OPERATOR, init=False)

    def can_view_all_incidents(self) -> bool:
        return False

    def can_assign_incident(self) -> bool:
        return False

    def can_change_incident_status(self) -> bool:
        return False

    def can_view_all_tasks(self) -> bool:
        return False

    def can_view_all_notifications(self) -> bool:
        return False


@dataclass
class Supervisor(User):
    """
    Rol intermedio. Puede ver todos los incidentes y tareas del sistema,
    asignar incidentes y cambiar su estado.
    """
    role: Role = field(default=Role.SUPERVISOR, init=False)

    def can_view_all_incidents(self) -> bool:
        return True

    def can_assign_incident(self) -> bool:
        return True

    def can_change_incident_status(self) -> bool:
        return True

    def can_view_all_tasks(self) -> bool:
        return True

    def can_view_all_notifications(self) -> bool:
        return False


@dataclass
class Admin(User):
    """
    Rol con permisos completos. Puede ver y gestionar todo el sistema,
    incluyendo usuarios, roles, incidentes, tareas y notificaciones.
    """
    role: Role = field(default=Role.ADMIN, init=False)

    def can_view_all_incidents(self) -> bool:
        return True

    def can_assign_incident(self) -> bool:
        return True

    def can_change_incident_status(self) -> bool:
        return True

    def can_view_all_tasks(self) -> bool:
        return True

    def can_view_all_notifications(self) -> bool:
        return True
