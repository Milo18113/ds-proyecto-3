from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.domain.enums.role import Role
from backend.infrastructure.auth.jwt_handler import (
    decode_access_token,
    InvalidTokenError,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependencia base de FastAPI: extrae y valida el token JWT.
    Retorna el payload completo (sub, role, exp).
    Todos los endpoints protegidos dependen de esta función.
    """
    try:
        return decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*allowed_roles: Role):
    """
    Factory de dependencias para restringir endpoints por rol.

    Uso en un endpoint:
        @router.patch("/{id}/assign")
        def assign(payload=Depends(require_roles(Role.ADMIN, Role.SUPERVISOR))):
            ...
    """
    def _check(payload: dict = Depends(get_current_user_payload)) -> dict:
        role = Role(payload["role"])
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de: "
                       f"{[r.value for r in allowed_roles]}.",
            )
        return payload
    return _check


# Shortcuts listos para usar en los endpoints
require_admin = require_roles(Role.ADMIN)
require_supervisor_or_admin = require_roles(Role.SUPERVISOR, Role.ADMIN)
require_any_role = require_roles(Role.OPERATOR, Role.SUPERVISOR, Role.ADMIN)