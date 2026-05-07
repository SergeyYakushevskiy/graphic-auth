def test_passpoints_serializer_precision():
    from src.application.serializer import PassPointsSerializer

    class P:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Seq:
        def __init__(self, points):
            self.points = points

    serializer = PassPointsSerializer()

    seq = Seq([P(1.2345, 6.7891), P(10.0, 20.0)])
    result = serializer.serialize(seq)

    assert result == b"1.23:6.79|10.00:20.00"