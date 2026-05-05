from src.presentation.factories.login import LoginFactory
from src.presentation.factories.registration import RegisterFactory


class AuthFlowController:
    def __init__(self, config, auth_service, user_id: str):
        self.config = config
        self.auth_service = auth_service
        self.user_id = user_id

        self.register_window = None
        self.login_window = None

    def start(self):
        if not self._user_exists():
            self._open_register()
        else:
            self._open_login()

    def _user_exists(self) -> bool:
        try:
            return self.auth_service.user_exists(self.user_id)
        except Exception:
            return False

    def _open_register(self):
        self.register_window = RegisterFactory.create(
            self.config,
            self.auth_service
        )

        self.register_window.register_success.connect(
            self._on_registered
        )

        self.register_window.show()

    def _on_registered(self):
        self.register_window.close()
        self._open_login()

    def _open_login(self):
        self.login_window = LoginFactory.create(
            self.config,
            self.auth_service
        )

        self.login_window.show()
