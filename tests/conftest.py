import pytest

class DummyPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@pytest.fixture
def point():
    return DummyPoint

@pytest.fixture
def valid_points():
    return [
        DummyPoint(-1, 1),
        DummyPoint(2, 23),
        DummyPoint(46, 3),
    ]