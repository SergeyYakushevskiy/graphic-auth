def test_auth_service_register_and_verify_success(valid_points):
    from src.application.service.auth_service import AuthService

    class FakeRepo:
        def __init__(self):
            self.data = {}

        def save(self, user_id, bg, verifier):
            self.data[user_id] = (bg, verifier)

        def load(self, user_id):
            return self.data.get(user_id)

    class Policy:
        def normalize(self, seq):
            return seq

    class FakeCrypto:
        def derive_verifier(self, user_id, password, data, background_id):
            class F:
                def __init__(self):
                    self.value = b"hash"
            return F()

    class P:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Seq:
        def __init__(self, points):
            self.points = points

    class Serializer:
        def serialize(self, seq):
            return b"data"

    service = AuthService(
        repo=FakeRepo(),
        policy=Policy(),
        crypto=FakeCrypto(),
        serializer=Serializer()
    )

    service.register("u1", valid_points, "pass", "bg")

    assert service.verify("u1", valid_points, "pass") is True


def test_auth_service_verify_fails_on_wrong_password(valid_points):
    from src.application.service.auth_service import AuthService

    class FakeRepo:
        def save(self, *args, **kwargs):
            pass

        def load(self, user_id):
            return ("bg", b"correct")

    class Policy:
        def normalize(self, seq):
            return seq

    class FakeCrypto:
        def derive_verifier(self, *args, **kwargs):
            class F:
                def __init__(self):
                    self.value = b"wrong"
            return F()

    class Serializer:
        def serialize(self, seq):
            return b"data"

    service = AuthService(
        repo=FakeRepo(),
        policy=Policy(),
        crypto=FakeCrypto(),
        serializer=Serializer()
    )

    result = service.verify("u1", valid_points, "pass")

    assert result is False