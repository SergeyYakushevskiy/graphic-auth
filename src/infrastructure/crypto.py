from argon2.low_level import hash_secret_raw, Type
from gostcrypto.gostcipher import new as gost_cipher_new, MODE_ECB
from gostcrypto.gosthash import new as gost_hash_new

from src.domain.crypto import DigestPort, KDFPort, MACPort

GOST_HASH_NAME = "streebog256"
GOST_HASH_MODE = 256 # bits
GOST_CMAC_NAME = "kuznechik"
CMAC_BLOCK_SIZE = 16 # bytes
CMAC_KEY_SIZE = 32 # bytes

ARGON2ID_TIME_COST = 3 # iterations
ARGON2ID_MEMORY_COST = 65536 # bits
ARGON2ID_PARALLELISM = 2 # parallel lanes count
ARGON2ID_HASH_LEN = 32 # bytes

# =========================
# Стрибог (ГОСТ Р 34.11-2012)
# =========================

class StreebogDigest(DigestPort):
    """
    Безключевой криптографический хэш на основе ГОСТ Р 34.11-2012 (Стрибог-256).

    Используется как:
    - компрессия входных данных
    - canonical digest перед MAC
    """

    def digest(self, data: bytes) -> bytes:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes-like")

        data = bytearray(data)
        h = gost_hash_new(
            name=GOST_HASH_NAME,
            mode=GOST_HASH_MODE
        )

        h.update(data)
        return h.digest()



# =========================
# CMAC (ГОСТ R 34.13-2015)
# =========================

class KuznechikCMAC(MACPort):
    """
    Имитовставка (CMAC) на базе ГОСТ Р 34.12-2015 (Кузнечик).

    Полностью ручная реализация CMAC (без MODE_MAC),
    чтобы сохранить контроль над примитивом.
    """

    def compute(self, key: bytes, data: bytes) -> bytes:
        if len(key) != CMAC_KEY_SIZE:
            raise ValueError("Wrong size of Kuznechik key")

        key = bytes(key)
        data = bytes(data)

        cipher = gost_cipher_new(
            GOST_CMAC_NAME,
            bytearray(key),
            MODE_ECB
        )

        # subkey generation
        zero = bytearray(CMAC_BLOCK_SIZE)
        l = cipher.encrypt(zero)

        k1 = self._dbl(l)
        k2 = self._dbl(k1)

        blocks = [
            data[i:i + CMAC_BLOCK_SIZE]
            for i in range(0, len(data), CMAC_BLOCK_SIZE)
        ]

        if not blocks:
            blocks = [self._pad(b"")]

        last_index = len(blocks) - 1

        if len(blocks[last_index]) == CMAC_BLOCK_SIZE:
            blocks[last_index] = self._xor(blocks[last_index], k1)
        else:
            blocks[last_index] = self._xor(
                self._pad(blocks[last_index]),
                k2
            )

        state = bytearray(CMAC_BLOCK_SIZE)

        for block in blocks:
            state = cipher.encrypt(
                self._xor(state, block)
            )

        return bytes(state)

    @staticmethod
    def _xor(a: bytes, b: bytes) -> bytearray:
        return bytearray(x ^ y for x, y in zip(a, b))

    @staticmethod
    def _pad(block: bytes) -> bytes:
        return block + b"\x80" + b"\x00" * (CMAC_BLOCK_SIZE - len(block) - 1)

    @staticmethod
    def _dbl(block: bytes) -> bytes:
        val = int.from_bytes(block, "big")

        if val & (1 << 127):
            val = ((val << 1) & ((1 << 128) - 1)) ^ 0x87
        else:
            val <<= 1

        return val.to_bytes(CMAC_BLOCK_SIZE, "big")


# =========================
# KDF (Argon2id)
# =========================

class Argon2idKDFAdapter(KDFPort):
    """
    Argon2id KDF (без изменений).
    """

    def __init__(self, config):
        self.config = config

    def derive(self, password: bytes, salt: bytes) -> bytes:
        return hash_secret_raw(
            secret=password,
            salt=salt,
            time_cost=self.config.time_cost,
            memory_cost=self.config.memory_cost,
            parallelism=self.config.parallelism,
            hash_len=self.config.hash_len,
            type=Type.ID
        )


