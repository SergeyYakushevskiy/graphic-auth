from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, field_validator

from src.infrastructure.config.settings import AppSettings


class Paths(BaseModel):
    base_dir: Path
    assets_dir: Path
    img_dir: Path
    config_file: Path
    shadow_file: Path
    master_key_file: Path

    @field_validator("*")
    @classmethod
    def to_path(cls, v):
        return Path(v)

@dataclass(frozen=True)
class MasterKey:
    version: str
    created_at: datetime
    algorithm: str
    nonce_b64: str
    key_hex: str

    def raw_key(self) -> bytes:
        return bytes.fromhex(self.key_hex)

class Secrets(BaseModel):
    master_key: MasterKey

@dataclass(frozen=True)
class AppConfig:
    settings: AppSettings
    paths: Paths
    secrets: Secrets