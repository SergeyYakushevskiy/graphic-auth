from abc import ABC, abstractmethod


class SecretRepository(ABC):

    @abstractmethod
    def save(self, user_id: str, verifier: bytes) -> None:
        pass

    @abstractmethod
    def load(self, user_id: str) -> bytes | None:
        pass
