from src.domain.model import PassPointSequence


COORD_PRECISION = 5
POINT_TEMPLATE = "{x:.{prec}f}:{y:.{prec}f}"


class PassPointsSerializer:
    def serialize(self, seq: PassPointSequence) -> bytes:
        return b"|".join(
            POINT_TEMPLATE.format(x=p.x, y=p.y, prec=COORD_PRECISION).encode()
            for p in seq.points
        )
