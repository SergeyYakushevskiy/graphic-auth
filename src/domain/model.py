from dataclasses import dataclass
from math import isfinite, hypot

EPS = 10.0

@dataclass(frozen=True)
class Point:
    x: float
    y: float

@dataclass(frozen=True)
class UserAuthData:
    user_id: str
    background_id: str
    verifier: bytes

@dataclass(frozen=True)
class PassPointSequence:
    points: tuple[Point, ...]

    def validate(self):
        if len(self.points) < 3:
            raise ValueError("Too few points")

        for p in self.points:
            if not (isfinite(p.x) and isfinite(p.y)):
                raise ValueError("Non-finite coordinate detected")

        # epsilon-based уникальность
        pts = self.points
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[i].x - pts[j].x
                dy = pts[i].y - pts[j].y

                if hypot(dx, dy) < EPS:
                    raise ValueError("Duplicate points (epsilon-equal)")
