from sqlalchemy import Column, String, DateTime, Enum as SAEnum
from datetime import datetime

from backend.infrastructure.orm.base import Base
from backend.domain.enums.role import Role


class UserModel(Base):
    """Modelo ORM para la tabla users."""
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SAEnum(Role, name="role_enum", create_constraint=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
