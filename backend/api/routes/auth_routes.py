from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.infrastructure.database.connection import get_db
from backend.infrastructure.auth.jwt_handler import create_access_token
from backend.infrastructure.auth.password_handler import verify_password
from backend.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from backend.api.guards.role_guard import get_current_user_payload

router = APIRouter(tags=["Auth"])


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class MeResponse(BaseModel):
    user_id: str
    role: str


def get_user_repo(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepositoryImpl = Depends(get_user_repo),
):
    """
    Autentica al usuario con username/password en formato OAuth2.
    En este proyecto, username será el email.
    """
    user = user_repo.find_by_email(form_data.username)

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
        )

    token = create_access_token(user_id=user.id, role=user.role)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        role=user.role.value,
    )


@router.get("/me", response_model=MeResponse)
def get_me(payload: dict = Depends(get_current_user_payload)):
    return MeResponse(
        user_id=payload["sub"],
        role=payload["role"],
    )
