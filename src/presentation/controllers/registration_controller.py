import getpass
import re
from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from src.application.service.auth_service import AuthService

from src.presentation.ui.windows.register import RegisterWindow
from src.presentation.ui.screens.password_screen import PasswordScreen
from src.presentation.ui.screens.background_screen import BackgroundScreen
from src.presentation.ui.screens.passpoints_screen import PasspointsScreen


class RegistrationController(QObject):
    def __init__(self, window: RegisterWindow, auth_service: AuthService):
        super().__init__()

        self.window = window
        self.auth_service = auth_service  # ✅ DI

        self.password_screen: PasswordScreen = window.password_screen
        self.background_screen: BackgroundScreen = window.background_screen
        self.passpoints_screen: PasspointsScreen = window.passpoints_screen

        self._password: str | None = None
        self._background: str | None = None
        self._points: list = []

        self._connect()

    def _connect(self):
        self.window.password_next.connect(self._on_password_next)
        self.window.background_next.connect(self._on_background_next)
        self.window.passpoints_next.connect(self._on_finish)
        self.window.background_back.connect(lambda: self.window.switch(0))
        self.window.passpoints_back.connect(lambda: self.window.switch(1))

    def _show_error(self, title: str, message: str):
        msg = QMessageBox(self.window)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def _validate_password(self, password: str) -> tuple[bool, str | None]:
        if not password:
            return False, "Пароль не может быть пустым"

        if len(password) < 8:
            return False, "Пароль должен быть не менее 8 символов"

        if not re.search(r"[A-Z]", password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву"

        if not re.search(r"[a-z]", password):
            return False, "Пароль должен содержать хотя бы одну строчную букву"

        if not re.search(r"\d", password):
            return False, "Пароль должен содержать хотя бы одну цифру"

        return True, None

    def _validate_points(self, points: list) -> tuple[bool, str | None]:
        if len(points) < 3:
            return False, "Нужно минимум 3 точки для графического пароля"

        return True, None

    def _on_password_next(self):
        password = self.password_screen.password_input.text()

        ok, error = self._validate_password(password)
        if not ok:
            self._show_error("Ошибка пароля", error or "Некорректный пароль")
            return

        self._password = password
        self.window.switch(1)

    def _on_background_next(self, path: str):
        if not path:
            self._show_error("Ошибка", "Фон не выбран")
            return

        self._background = path

        self.window.passpoints_screen.canvas.set_background(QPixmap(path))
        self.window.switch(2)

    def _on_finish(self, points: list):
        ok, error = self._validate_points(points)
        if not ok:
            self._show_error("Ошибка", error or "Некорректные точки")
            return

        self._points = points
        self._complete_registration()

    def _extract_background_id(self, path: str) -> str:
        return Path(path).stem

    def _complete_registration(self):
        if not self._password or not self._background or not self._points:
            self._show_error("Ошибка", "Неполные данные")
            return

        try:
            background_id = self._extract_background_id(self._background)

            user_id = getpass.getuser()

            self.auth_service.register(
                user_id=user_id,
                raw_points=self._points,
                password=self._password,
                background_id=background_id
            )

            QMessageBox.information(
                self.window,
                "Успех",
                "Регистрация завершена"
            )
            self.window.register_success.emit()
        except Exception as e:
            self._show_error("Ошибка регистрации", str(e))
