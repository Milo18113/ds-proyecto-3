from typing import Optional
from sqlalchemy.orm import Session

from backend.domain.entities.user import User, Operator, Supervisor, Admin
from backend.domain.repositories.user_repository import UserRepository
from backend.domain.enums.role import Role
from backend.infrastructure.orm.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """Implementación concreta del repositorio de usuarios usando SQLAlchemy ORM."""

    def __init__(self, db: Session):
        self.db = db

    # ── Mappers ───────────────────────────────────────────────────────────

    def _to_domain(self, model: UserModel) -> User:
        """Retorna la subclase correcta de User según el rol."""
        cls_map = {
            Role.ADMIN: Admin,
            Role.SUPERVISOR: Supervisor,
            Role.OPERATOR: Operator,
        }
        cls = cls_map[model.role]
        return cls(
            id=model.id,
            name=model.name,
            email=model.email,
            hashed_password=model.hashed_password,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            hashed_password=entity.hashed_password,
            role=entity.role,
            created_at=entity.created_at,
        )

    # ── CRUD ──────────────────────────────────────────────────────────────

    def save(self, user: User) -> User:
        model = self._to_model(user)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def find_by_id(self, user_id: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(model) if model else None

    def find_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(model) if model else None

    def find_all(self) -> list[User]:
        models = self.db.query(UserModel).all()
        return [self._to_domain(m) for m in models]
