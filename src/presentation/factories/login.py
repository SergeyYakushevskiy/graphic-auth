from src.application.service.auth_service import AuthService
from src.presentation.ui.windows.login import LoginWindow
from src.presentation.controllers.login_controller import LoginController


class LoginFactory:

    @staticmethod
    def create(config, auth_service: AuthService) -> LoginWindow:

        window = LoginWindow(config)
        controller = LoginController(window, auth_service)

        window._controller = controller

        return window
