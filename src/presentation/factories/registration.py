from src.application.service.auth_service import AuthService
from src.infrastructure.config.types import AppConfig
from src.presentation.ui.windows.register import RegisterWindow
from src.presentation.controllers.registration_controller import RegistrationController


class RegisterFactory:

    @staticmethod
    def create(config : AppConfig, auth_service : AuthService) -> RegisterWindow:

        window = RegisterWindow(config)
        controller = RegistrationController(window, auth_service)

        window._controller = controller

        return window
