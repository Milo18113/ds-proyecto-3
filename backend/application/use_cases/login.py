from backend.domain.repositories.user_repository import UserRepository
from backend.infrastructure.auth.password_handler import verify_password
from backend.infrastructure.auth.jwt_handler import create_access_token
from backend.application.dtos.user_dto import LoginDTO, TokenDTO


class LoginUseCase:
    """
    Caso de uso: autenticación de usuario.
    Valida credenciales y retorna un JWT.
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, dto: LoginDTO) -> TokenDTO:
        user = self.user_repo.find_by_email(dto.email)
        if not user:
            raise ValueError("Credenciales inválidas.")

        if not verify_password(dto.password, user.hashed_password):
            raise ValueError("Credenciales inválidas.")

        token = create_access_token(
            data={"sub": user.id, "role": user.role.value}
        )

        return TokenDTO(access_token=token)
