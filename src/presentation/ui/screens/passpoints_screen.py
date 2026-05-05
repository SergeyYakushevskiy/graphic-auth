from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from src.presentation.ui.features.passpoints_canvas import PasspointsCanvas


class PasspointsScreen(QWidget):
    back_clicked = Signal()
    finish_clicked = Signal(list)

    def __init__(self):
        super().__init__()

        self.selected_path: str | None = None
        self._background_pixmap = None

        self._build()

        if self._background_pixmap:
            self.canvas.set_background(self._background_pixmap)

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(60, 40, 60, 0)

        title = QLabel("Укажите графический пароль в виде точек")
        title.setStyleSheet("color: white; font-size: 24px; background: transparent")

        self.canvas = PasspointsCanvas(self)
        self.canvas.setMinimumHeight(400)
        self.canvas.setSizePolicy(
            self.canvas.sizePolicy().horizontalPolicy(),
            self.canvas.sizePolicy().verticalPolicy()
        )

        content_layout.addWidget(title)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.canvas, 1)
        content_layout.addStretch()

        content_wrapper = QHBoxLayout()
        content_wrapper.addStretch()
        content_wrapper.addLayout(content_layout)
        content_wrapper.addStretch()

        nav_layout = QHBoxLayout()

        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedWidth(140)
        self.btn_back.clicked.connect(self.back_clicked.emit)

        self.btn_clear = QPushButton("Очистить")
        self.btn_clear.setFixedWidth(140)
        self.btn_clear.clicked.connect(self.canvas.reset)

        self.btn_finish = QPushButton("Завершить")
        self.btn_finish.setFixedWidth(140)
        self.btn_finish.clicked.connect(self._on_finish_click)

        btn_style = """
            QPushButton {
                padding: 8px;
                font-size: 14px;
            }
        """

        self.btn_back.setStyleSheet(btn_style)
        self.btn_clear.setStyleSheet(btn_style)
        self.btn_finish.setStyleSheet(btn_style)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_clear)
        nav_layout.addWidget(self.btn_finish)

        root.addLayout(content_wrapper)
        root.addStretch()
        root.addLayout(nav_layout)

    def set_background(self, path: str):
        self._background_pixmap = QPixmap(path)

        self.setStyleSheet(f"""
            PasspointsScreen {{
                background-image: url({path});
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)

        if hasattr(self, "canvas"):
            self.canvas.set_background(self._background_pixmap)

    def reset_background(self):
        self.selected_path = None
        self._background_pixmap = None
        self.canvas.reset()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        margin_x = 60
        margin_top = 100
        margin_bottom = 120

        self.canvas.setGeometry(
            margin_x,
            margin_top,
            self.width() - margin_x * 2,
            self.height() - margin_top - margin_bottom
        )

    def _on_finish_click(self):
        self.finish_clicked.emit(self.canvas.get_points())
