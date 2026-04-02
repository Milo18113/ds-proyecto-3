from pydantic import BaseModel
from datetime import datetime

from backend.domain.enums.role import Role


class UserResponseDTO(BaseModel):
    """DTO de respuesta para un usuario."""
    id: str
    name: str
    email: str
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True


class LoginDTO(BaseModel):
    """DTO de entrada para login."""
    email: str
    password: str


class TokenDTO(BaseModel):
    """DTO de respuesta con el token JWT."""
    access_token: str
    token_type: str = "bearer"
