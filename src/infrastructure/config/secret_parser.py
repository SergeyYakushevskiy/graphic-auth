from datetime import datetime, timezone

from .types import MasterKey


class MasterKeyParser:

    def parse(self, raw: bytes) -> MasterKey:
        text = raw.decode("utf-8").strip()
        parts = text.split("|")

        if len(parts) != 5:
            raise ValueError("Invalid master key format")

        version, ts, algo, nonce_b64, key_hex = parts

        created_at = datetime.fromisoformat(ts)

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        if not key_hex:
            raise ValueError("Empty key material")

        return MasterKey(
            version=version,
            created_at=created_at,
            algorithm=algo,
            nonce_b64=nonce_b64,
            key_hex=key_hex
        )
