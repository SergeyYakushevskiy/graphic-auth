from src.application.serializer import PassPointsSerializer
from src.application.service.crypto_service import CryptoService
from src.domain.model import PassPointSequence
from src.domain.policy import TolerancePolicy
from src.domain.storage import SecretRepository


class AuthService:
    def __init__(self,
                 repo : SecretRepository,
                 policy : TolerancePolicy,
                 crypto : CryptoService,
                 serializer: PassPointsSerializer):
        self.repo = repo
        self.policy = policy
        self.crypto = crypto
        self.serializer = serializer

    def user_exists(self, user_id: str) -> bool:
        return self.repo.load(user_id) is not None

    def register(self, user_id : str, raw_points : list, password : str, background_id : str):
        seq = PassPointSequence(tuple(raw_points))
        seq.validate()
        norm = self.policy.normalize(seq)
        data = self.serializer.serialize(norm)
        fingerprint = self.crypto.derive_verifier(user_id=user_id, password=password, data=data, background_id=background_id)
        self.repo.save(user_id, background_id, fingerprint.value)

    def verify(self, user_id, raw_points, password):
        stored = self.repo.load(user_id)
        if stored is None:
            return False
        background_id, verifier = stored
        seq = PassPointSequence(tuple(raw_points))
        seq.validate()
        norm = self.policy.normalize(seq)
        data = self.serializer.serialize(norm)

        candidate = self.crypto.derive_verifier(user_id, password, data, background_id).value
        return candidate == verifier
