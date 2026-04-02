from abc import ABC, abstractmethod
from typing import Optional
from backend.domain.entities.user import User


class UserRepository(ABC):
    """Puerto de salida para persistencia de usuarios."""

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    def save(self, user: User) -> User:
        ...

    @abstractmethod
    def find_all(self) -> list[User]:
        ...
