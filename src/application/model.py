from dataclasses import dataclass


@dataclass(frozen=True)
class PassPointsFingerprint:
    value: bytes
