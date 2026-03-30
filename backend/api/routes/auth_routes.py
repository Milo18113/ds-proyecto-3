from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend.infrastructure.auth.jwt_handler import create_access_token
from backend.infrastructure.auth.password_handler import verify_password
from backend.api.guards.role_guard import get_current_user_payload
from backend.domain.enums.role import Role

router = APIRouter(tags=["Auth"])


# ── DTOs de entrada y salida ──────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class MeResponse(BaseModel):
    user_id: str
    role: str


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, user_repo=Depends(lambda: _get_user_repo())):
    """
    Autentica al usuario con email y contraseña.
    Si las credenciales son válidas retorna un JWT.
    """
    user = user_repo.find_by_email(body.email)

    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
        )

    token = create_access_token(user_id=user.id, role=user.role)
    return LoginResponse(access_token=token, role=user.role.value)


@router.get("/me", response_model=MeResponse)
def get_me(payload: dict = Depends(get_current_user_payload)):
    """
    Retorna el ID y rol del usuario autenticado actual.
    Útil para que el frontend sepa qué vistas mostrar.
    """
    return MeResponse(user_id=payload["sub"], role=payload["role"])


# ── Inyección de dependencia (se reemplaza con el repo real en main.py) ──

def _get_user_repo():
    """
    Placeholder — en main.py se sobrescribe con la implementación real
    de UserRepository usando SQLAlchemy.
    """
    raise NotImplementedError("UserRepository no configurado.")