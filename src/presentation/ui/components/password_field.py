from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt


class PasswordField(QLineEdit):
    """
    Linux-style password input field.
    Minimal, secure-looking UI component.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self):
        self.setEchoMode(QLineEdit.Password)

        self.setFixedHeight(38)

        self.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 20, 20, 0.95);
                color: #E6E6E6;

                border: 1px solid #3A3A3A;
                border-radius: 10px;

                padding-left: 10px;
                padding-right: 10px;

                font-size: 14px;
                font-family: "DejaVu Sans Mono", "Consolas", monospace;
            }

            QLineEdit:focus {
                border: 1px solid #5A9FD4;
                background-color: rgba(25, 25, 25, 0.98);
            }
        """)

        self.setPlaceholderText("Введите пароль")
