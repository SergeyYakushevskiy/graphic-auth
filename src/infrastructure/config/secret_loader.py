from pathlib import Path

from src.infrastructure.config.secret_parser import MasterKeyParser
from src.infrastructure.config.types import Secrets


def load_master_key(path: Path, parser: MasterKeyParser) -> Secrets:
    if not path.exists():
        raise RuntimeError(f"Master key not found: {path}")

    raw = path.read_bytes()
    key = parser.parse(raw)

    return Secrets(master_key=key)
