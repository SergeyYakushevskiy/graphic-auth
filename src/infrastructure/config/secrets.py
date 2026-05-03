from pathlib import Path


class SecretProvider:
    """
    Абстракция источника секретов.
    """

    def get_master_key(self) -> bytes:
        raise NotImplementedError


class FileSecretProvider(SecretProvider):

    def __init__(self, path: Path):
        self.path = path

    def get_master_key(self) -> bytes:
        if not self.path.exists():
            raise RuntimeError("Master key file not found")

        data = self.path.read_bytes()

        if len(data) != 32:
            raise RuntimeError("Invalid master key size")

        return data


class DevFallbackSecretProvider(SecretProvider):
    """
    Только для dev. Явно небезопасно.
    """

    def get_master_key(self) -> bytes:
        return b"\x00" * 32
