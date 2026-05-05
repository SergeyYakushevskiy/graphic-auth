from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from src.infrastructure.config.types import AppConfig
from src.presentation.ui.components.background_picker import BackgroundImagePicker


class BackgroundScreen(QWidget):
    next_clicked = Signal(str)
    back_clicked = Signal()

    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
        self.selected_path: str | None = None
        self._build()

    def _build(self):
        root = QVBoxLayout(self)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(60, 40, 60, 0)

        title = QLabel("Выберите фон")
        title.setStyleSheet("color: white; font-size: 24px;")

        self.background_picker = BackgroundImagePicker(self.config)

        self.background_picker.image_selected.connect(self._on_image_selected)

        content_layout.addWidget(title)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.background_picker)
        content_layout.addStretch()

        content_wrapper = QHBoxLayout()
        content_wrapper.addStretch()
        content_wrapper.addLayout(content_layout)
        content_wrapper.addStretch()

        nav_layout = QHBoxLayout()

        self.btn_back = QPushButton("← Назад")
        self.btn_back.setFixedWidth(140)
        self.btn_back.clicked.connect(self.back_clicked.emit)

        self.btn_next = QPushButton("Далее →")
        self.btn_next.setFixedWidth(140)
        self.btn_next.clicked.connect(self._on_next)

        self.btn_next.setEnabled(False)  # 🔥 важно

        btn_style = """
            QPushButton {
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:disabled {
                color: #777;
            }
        """

        self.btn_back.setStyleSheet(btn_style)
        self.btn_next.setStyleSheet(btn_style)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)

        root.addLayout(content_wrapper)
        root.addStretch()
        root.addLayout(nav_layout)

    def _on_image_selected(self, path: str):
        self.selected_path = path
        self.btn_next.setEnabled(True)

    def _on_next(self):
        if not self.selected_path:
            return

        self.next_clicked.emit(self.selected_path)

