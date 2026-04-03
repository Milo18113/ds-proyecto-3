from abc import ABC, abstractmethod
from backend.domain.entities.user import User


class UserRepository(ABC):
    """
    Puerto de salida para persistencia de usuarios.
    La implementación concreta vive en infrastructure/repositories/.
    """

    @abstractmethod
    def save(self, user: User) -> None:
        """Persiste un usuario nuevo o actualiza uno existente."""
        ...

    @abstractmethod
    def find_by_id(self, user_id: str) -> User | None:
        """Retorna un usuario por su ID, o None si no existe."""
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """Retorna un usuario por su email, o None si no existe.
        Usado principalmente en el flujo de login."""
        ...

    @abstractmethod
    def find_all(self) -> list[User]:
        """Retorna todos los usuarios del sistema."""
        ...

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """Elimina un usuario por su ID."""
        ...