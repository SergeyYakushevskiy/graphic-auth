from dataclasses import dataclass
from math import sqrt
from .model import Point, PassPointSequence

MIN_SCALE: float = 0.03
STEP = 0.08

@dataclass(frozen=True)
class TolerancePolicy:

    def normalize(self, seq: PassPointSequence) -> PassPointSequence:
        pts = seq.points

        cx = sum(p.x for p in pts) / len(pts)
        cy = sum(p.y for p in pts) / len(pts)

        centered = [(p.x - cx, p.y - cy) for p in pts]

        scale = sqrt(sum(x*x + y*y for x, y in centered) / len(centered))
        if scale < MIN_SCALE:
            scale = MIN_SCALE

        norm = tuple(
            Point(x / scale, y / scale)
            for x, y in centered
        )

        return self._quantize(norm)

    def _quantize(self, seq : tuple):
        return PassPointSequence(
            tuple(
                Point(
                    round(p.x / STEP) * STEP,
                    round(p.y / STEP) * STEP
                )
                for p in seq
            )
        )