from abc import ABC, abstractmethod
from backend.domain.events.base_event import DomainEvent


class Observer(ABC):
    @abstractmethod
    def update(self, event: DomainEvent) -> None:
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"