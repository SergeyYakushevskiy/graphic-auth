import os
import tomllib
from pathlib import Path

from .paths import resolve_paths
from .secret_loader import load_master_key
from .secret_parser import MasterKeyParser
from .settings import AppSettings
from .types import AppConfig


def load():
    env = os.getenv("APP_ENV", "dev")
    project_dir = Path.cwd()

    paths = resolve_paths(env, project_dir)

    settings = _load_settings(paths.config_file)

    parser = MasterKeyParser()
    secrets = load_master_key(paths.master_key_file, parser)

    return AppConfig(settings, paths, secrets)

def _load_settings(path: Path) -> AppSettings:
    if not path.exists():
        raise RuntimeError(f"Config file not found: {path}")

    with open(path, "rb") as f:
        raw = tomllib.load(f)

    return AppSettings.model_validate(raw)

