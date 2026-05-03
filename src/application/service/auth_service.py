import hmac

from src.domain.model import PassPointSequence


class AuthService:
    def __init__(self, repo, policy, crypto, serializer):
        self.repo = repo
        self.policy = policy
        self.crypto = crypto
        self.serializer = serializer

    def register(self, user_id, raw_points, password):
        seq = PassPointSequence(tuple(raw_points))
        norm = self.policy.normalize(seq)

        data = self.serializer.serialize(norm)

        fingerprint = self.crypto.derive_verifier(user_id, password, data)
        self.repo.save(user_id, fingerprint.value)

    def verify(self, user_id, raw_points, password):
        stored = self.repo.load(user_id)
        if stored is None:
            return False

        seq = PassPointSequence(tuple(raw_points))
        norm = self.policy.normalize(seq)

        data = self.serializer.serialize(norm)

        candidate = self.crypto.derive_verifier(user_id, password, data).value

        return hmac.compare_digest(candidate, stored)
