from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Abstracción del patrón Command.
    """

    @abstractmethod
    def execute(self) -> None:
        ...