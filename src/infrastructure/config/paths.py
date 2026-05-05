from pathlib import Path
from .types import Paths


def resolve_paths(env: str, project_dir: Path) -> Paths:
    if env == "prod":
        base_dir = Path("/var/lib/graph-auth")
        assets_dir = project_dir / "assets"
        img_dir = assets_dir / "img"
        return Paths(
            base_dir=base_dir,
            assets_dir=assets_dir,
            config_file=base_dir / "config.toml",
            shadow_file=Path("/etc/shadow.ga"),
            master_key_file=Path("/etc/secret/master.key"),
            img_dir=img_dir
        )

    base_dir = project_dir
    assets_dir = project_dir / "assets"
    img_dir = assets_dir / "img"

    return Paths(
        base_dir=base_dir,
        assets_dir=base_dir / "assets",
        config_file=base_dir / "config.toml",
        shadow_file=base_dir / "shadow.ga",
        master_key_file=(base_dir / "assets" / "master.key"),
        img_dir=img_dir
    )
