from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from src.presentation.ui.components.password_field import PasswordField


class PasswordScreen(QWidget):
    next_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):

        root = QVBoxLayout(self)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(60, 40, 60, 0)

        title = QLabel("Укажите пароль")
        title.setStyleSheet("color: white; font-size: 24px;")

        self.password_input = PasswordField()
        self.password_input.setFixedWidth(320)

        content_layout.addWidget(title)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignLeft)

        content_layout.addStretch()

        content_wrapper = QHBoxLayout()
        content_wrapper.addLayout(content_layout)
        content_wrapper.addStretch()

        nav_layout = QHBoxLayout()

        nav_layout.addStretch()

        btn_next = QPushButton("Далее")
        btn_next.setFixedWidth(140)
        btn_next.clicked.connect(self.next_clicked.emit)

        btn_next.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 14px;
            }
        """)

        nav_layout.addWidget(btn_next)

        root.addLayout(content_wrapper)
        root.addStretch()
        root.addLayout(nav_layout)

    def get_password(self) -> str:
        return self.password_input.text().strip()
