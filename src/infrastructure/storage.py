import os
import tempfile
from pathlib import Path

from src.domain.storage import SecretRepository

FILE_MODE = 0o600


class FileSecretRepository(SecretRepository):
    """
    Shadow-like storage:

    user_id:verifier_hex
    """

    def __init__(self, shadow_path: Path):
        self.shadow_path = shadow_path
        self._ensure_storage()

    def save(self, user_id: str, verifier: bytes) -> None:
        data = self._load_all()
        data[user_id] = verifier.hex()
        self._atomic_write(data)

    def load(self, user_id: str) -> bytes | None:
        data = self._load_all()
        record = data.get(user_id)

        if record is None:
            return None

        return bytes.fromhex(record)

    def _ensure_storage(self) -> None:
        self.shadow_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.shadow_path.exists():
            self.shadow_path.touch(mode=FILE_MODE, exist_ok=True)
        else:
            os.chmod(self.shadow_path, FILE_MODE)

    def _load_all(self) -> dict[str, str]:
        result: dict[str, str] = {}

        try:
            with open(self.shadow_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(":", 1)
                    if len(parts) != 2:
                        continue

                    user_id, verifier_hex = parts
                    result[user_id] = verifier_hex

        except FileNotFoundError:
            return {}

        return result

    def _atomic_write(self, data: dict[str, str]) -> None:
        dir_name = os.path.dirname(self.shadow_path) or "."

        fd, tmp_path = tempfile.mkstemp(dir=dir_name)
        try:
            with os.fdopen(fd, "w") as tmp:
                for user_id, verifier_hex in data.items():
                    tmp.write(f"{user_id}:{verifier_hex}\n")

            os.chmod(tmp_path, FILE_MODE)
            os.replace(tmp_path, self.shadow_path)

            tmp_path = None

        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)


