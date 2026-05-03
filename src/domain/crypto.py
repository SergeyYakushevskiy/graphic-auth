from abc import ABC, abstractmethod


class DigestPort(ABC):
    """
    Абстракция криптографического примитива свёртки данных в фиксированный отпечаток.

    Поддерживает:
    - безключевые хэш-функции (например, ГОСТ Р 34.11-2012 / Стрибог)
    - keyed-доменные конструкции при необходимости (через фиксированный внутренний ключ)
    - использование как входного примитива для KDF/MAC схем
    """

    @abstractmethod
    def digest(self, data: bytes) -> bytes:
        pass



class KDFPort(ABC):
    """
    Абстракция KDF (Argon2id).
    """

    @abstractmethod
    def derive(self, password: bytes, salt: bytes) -> bytes:
        pass


class MACPort(ABC):
    """
    Абстракция MAC
    """

    @abstractmethod
    def compute(self, key: bytes, data: bytes) -> bytes:
        pass