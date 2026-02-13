from abc import ABC, abstractmethod


class Connector(ABC):
    name: str

    @abstractmethod
    def fetch(self) -> dict:
        raise NotImplementedError
