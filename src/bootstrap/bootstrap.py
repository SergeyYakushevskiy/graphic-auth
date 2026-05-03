from src.application.serializer import PassPointsSerializer
from src.application.service.auth_service import AuthService
from src.application.service.crypto_service import CryptoService
from src.bootstrap.container import Container
from src.domain.crypto import DigestPort, KDFPort, MACPort
from src.domain.policy import TolerancePolicy
from src.domain.storage import SecretRepository
from src.infrastructure.config.loader import load
from src.infrastructure.config.settings import Argon2Config
from src.infrastructure.config.types import AppConfig
from src.infrastructure.crypto import Argon2idKDFAdapter, KuznechikCMAC, StreebogDigest
from src.infrastructure.storage import FileSecretRepository


def build_container():
    container = Container()

    config: AppConfig = load()

    container.singleton(
        AppConfig,
        lambda c: config
    )

    container.singleton(
        Argon2Config,
        lambda c: c.resolve(AppConfig).settings.argon2
    )

    container.singleton(
        SecretRepository,
        lambda c: FileSecretRepository(config.paths.shadow_file)
    )

    container.singleton(
        TolerancePolicy,
        lambda c: TolerancePolicy()
    )

    container.singleton(
        DigestPort,
        lambda c: StreebogDigest()
    )

    container.singleton(
        KDFPort,
        lambda c: Argon2idKDFAdapter(
            c.resolve(Argon2Config)
        )
    )

    container.singleton(
        MACPort,
        lambda c: KuznechikCMAC()
    )

    container.singleton(
        CryptoService,
        lambda c: CryptoService(
            hasher=c.resolve(DigestPort),
            kdf=c.resolve(KDFPort),
            mac=c.resolve(MACPort),
            master_key=c.resolve(AppConfig).secrets.master_key
        )
    )

    container.singleton(
        PassPointsSerializer,
        lambda c: PassPointsSerializer()
    )

    container.singleton(
        AuthService,
        lambda c: AuthService(
            repo=c.resolve(SecretRepository),
            policy=c.resolve(TolerancePolicy),
            crypto=c.resolve(CryptoService),
            serializer=c.resolve(PassPointsSerializer)
        )
    )

    return container
