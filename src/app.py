import getpass
import sys

from PySide6.QtWidgets import QApplication

from src.application.service.auth_service import AuthService
from src.bootstrap.bootstrap import build_container
from src.infrastructure.config.types import AppConfig
from src.presentation.controllers.flow_controller import AuthFlowController


def main():
    app = QApplication(sys.argv)

    container = build_container()
    config: AppConfig = container.resolve(AppConfig)
    auth_service: AuthService = container.resolve(AuthService)

    user_id = getpass.getuser()

    controller = AuthFlowController(
        config=config,
        auth_service=auth_service,
        user_id=user_id,
    )

    controller.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
