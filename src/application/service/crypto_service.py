from src.application.model import PassPointsFingerprint
from src.infrastructure.config.types import MasterKey

STRING_ENCODING = 'utf-8'
VERSION = b"pp:v1" # версия алгоритма деривации


class CryptoService:

    def __init__(self, hasher, kdf, mac, master_key: MasterKey):
        self.hasher = hasher
        self.kdf = kdf
        self.mac = mac
        self.master_key = master_key

    def derive_verifier(self, user_id: str, password: str, data: bytes):
        """
        Функция формирования производной от аутентификационных данных

        Стадии:
        1. Хеш: разделение домена + привязка данных
        2. MAC: слой привязки к мастер-ключу
        3. Формирование соли: пользовательский контекст + выход MAC
        4. KDF: усиление пароля (Argon2id)
        """

        digest = self.hasher.digest(VERSION + data)

        mac_value = self.mac.compute(
            self.master_key.raw_key(),
            digest
        )

        salt = user_id.encode(STRING_ENCODING) + mac_value

        key = self.kdf.derive(
            password.encode(STRING_ENCODING),
            salt
        )

        return PassPointsFingerprint(key)
