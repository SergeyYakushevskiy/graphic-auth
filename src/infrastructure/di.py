from punq import Container

from src.application.serializer import PassPointsSerializer
from src.application.service.auth_service import AuthService
from src.application.service.crypto_service import CryptoService

from src.domain.policy import TolerancePolicy
from src.domain.storage import SecretRepository
from src.domain.crypto import DigestPort, KDFPort, MACPort

from src.infrastructure.config.types import AppConfig
from src.infrastructure.config.settings import Argon2Config

from src.infrastructure.crypto import (
    StreebogDigest,
    Argon2idKDFAdapter,
    KuznechikCMAC
)

from src.infrastructure.storage import FileSecretRepository


def build_container(config: AppConfig) -> Container:
    container = Container()

    container.register(AppConfig, instance=config)
    container.register(Argon2Config, instance=config.settings.argon2)

    container.register(
        SecretRepository,
        instance=FileSecretRepository(
            shadow_path=config.paths.shadow_file
        )
    )

    container.register(TolerancePolicy)
    container.register(PassPointsSerializer)

    container.register(DigestPort, StreebogDigest)
    container.register(MACPort, KuznechikCMAC)

    container.register(
        KDFPort,
        factory=lambda: Argon2idKDFAdapter(config.settings.argon2)
    )

    container.register(
        CryptoService,
        factory=lambda: CryptoService(
            hasher=container.resolve(DigestPort),
            kdf=container.resolve(KDFPort),
            mac=container.resolve(MACPort),
            master_key=config.secrets.master_key
        )
    )

    container.register(
        AuthService,
        factory=lambda: AuthService(
            repo=container.resolve(SecretRepository),
            policy=container.resolve(TolerancePolicy),
            crypto=container.resolve(CryptoService),
            serializer=container.resolve(PassPointsSerializer),
        )
    )

    return container
