import getpass

from PySide6.QtCore import QObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from src.application.service.auth_service import AuthService
from src.presentation.ui.windows.login import LoginWindow


class LoginController(QObject):

    def __init__(self, window: LoginWindow, auth_service: AuthService):
        super().__init__()

        self.window = window
        self.auth_service = auth_service
        self._password: str | None = None
        self._points: list = []

        self._connect()

    def _connect(self):
        self.window.password_submitted.connect(self._on_password)
        self.window.points_submitted.connect(self._on_points)
        self.window.passpoints_back.connect(lambda : self.window.switch(0))

    def _validate_password(self, password: str) -> tuple[bool, str | None]:
        if not password:
            return False, "Пароль не может быть пустым"

        if len(password) < 8:
            return False, "Пароль должен быть не менее 8 символов"

        return True, None

    def _validate_points(self, points: list) -> tuple[bool, str | None]:
        if len(points) < 3:
            return False, "Недостаточно точек"

        return True, None

    def _on_password(self):
        password = self.window.password_screen.get_password()
        ok, error = self._validate_password(password)
        if not ok:
            self._show_error("Ошибка пароля", error)
            return

        self._password = password

        user_id = getpass.getuser()

        record = self.auth_service.repo.load(user_id)
        if not record:
            self._show_error("Ошибка", "Пользователь не найден")
            return

        background_id, _ = record

        path = self._resolve_background_path(background_id)

        self.window.passpoints_screen.canvas.set_background(QPixmap(path))
        self.window.switch(1)

    def _resolve_background_path(self, background_id: str) -> str:
        base = self.window.config.paths.img_dir / "auth"
        return str(base / f"{background_id}.jpg")

    def _on_points(self, points: list):
        ok, error = self._validate_points(points)
        if not ok:
            self._show_error("Ошибка графического пароля", error)
            return

        self._points = points
        self._authenticate()

    def _authenticate(self):
        if not self._password or not self._points:
            self._show_error("Ошибка", "Неполные данные")
            return

        try:
            user_id = getpass.getuser()

            success = self.auth_service.verify(
                user_id=user_id,
                raw_points=self._points,
                password=self._password
            )

            if not success:
                self._show_error("Ошибка входа", "Неверный пароль или графический ключ")
                return

            QMessageBox.information(
                self.window,
                "Успех",
                f"Авторизация завершена. Пользователь: {user_id}"
            )

        except Exception as e:
            self._show_error("Ошибка", str(e))

    def _show_error(self, title: str, message: str):
        msg = QMessageBox(self.window)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
