from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from backend.application.use_cases.login import LoginUseCase
from backend.application.dtos.user_dto import LoginDTO
from backend.api.guards.role_guard import get_current_user_payload

router = APIRouter(tags=["Auth"])


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class MeResponse(BaseModel):
    user_id: str
    role: str


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Autentica al usuario con username/password en formato OAuth2.
    Delega toda la lógica al LoginUseCase.
    """
    user_repo = UserRepositoryImpl(db)
    use_case = LoginUseCase(user_repo)

    dto = LoginDTO(
        email=(form_data.username or "").strip().lower(),
        password=form_data.password,
    )

    try:
        token_dto, role = use_case.execute(dto)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
        )

    return LoginResponse(
        access_token=token_dto.access_token,
        token_type=token_dto.token_type,
        role=role.value,
    )


@router.get("/me", response_model=MeResponse)
def get_me(payload: dict = Depends(get_current_user_payload)):
    return MeResponse(
        user_id=payload["sub"],
        role=payload["role"],
    )
