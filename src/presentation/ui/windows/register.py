from PySide6.QtCore import QPropertyAnimation, Signal
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QStackedWidget, QGraphicsOpacityEffect
)

from src.infrastructure.config.types import AppConfig
from src.presentation.ui.screens.background_screen import BackgroundScreen
from src.presentation.ui.screens.passpoints_screen import PasspointsScreen
from src.presentation.ui.screens.password_screen import PasswordScreen


class RegisterWindow(QMainWindow):
    register_success = Signal()
    password_next = Signal()
    background_next = Signal(str)
    background_back = Signal()
    passpoints_back = Signal()
    passpoints_next = Signal(list)

    def __init__(self, config: AppConfig):
        super().__init__()

        self.config = config
        self.default_background = self.config.paths.assets_dir / "img" / "main.jpg"
        self.selected_background: str | None = None
        self._init_ui()
        self._build_screens()
        self.selected_background: str | None = None

    def _init_ui(self):
        screen = QGuiApplication.primaryScreen().geometry()

        self.window_width = int(screen.width() * 0.75)
        self.window_height = int(screen.height() * 0.75)

        self.setWindowTitle("Passpoints аутентификация")
        self.setFixedSize(self.window_width, self.window_height)

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.root_layout = QVBoxLayout(self.central)
        self.root_layout.setContentsMargins(0, 0, 0, 0)

        self.background = QLabel(self.central)
        self.background.setScaledContents(True)

        main_path = self.config.paths.assets_dir / "img" / "main.jpg"
        pixmap = QPixmap(str(main_path))

        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.window_width, self.window_height)
        self.background.lower()

        self.overlay = QWidget(self.central)
        self.overlay.setStyleSheet("background-color: rgba(0,0,0,0.35);")
        self.overlay.setGeometry(0, 0, self.window_width, self.window_height)

        self.overlay_layout = QVBoxLayout(self.overlay)

        self.stack = QStackedWidget()
        self.overlay_layout.addWidget(self.stack)

    def _build_screens(self):
        self.password_screen = PasswordScreen()
        self.background_screen = BackgroundScreen(self.config)
        self.passpoints_screen = PasspointsScreen()

        self.stack.addWidget(self.password_screen)
        self.stack.addWidget(self.background_screen)
        self.stack.addWidget(self.passpoints_screen)

        self.password_screen.next_clicked.connect(self.password_next.emit)

        self.background_screen.next_clicked.connect(self.background_next.emit)
        self.background_screen.back_clicked.connect(self.background_back.emit)
        self.passpoints_screen.finish_clicked.connect(self.passpoints_next)
        self.passpoints_screen.back_clicked.connect(self.passpoints_back.emit)

        self.background_screen.background_picker.image_selected.connect(self._on_background_selected)

        self.stack.setCurrentIndex(0)

    def switch(self, index: int):
        self._fade_to(index)

    def _on_background_selected(self, path: str):
        self.selected_background = path

    def _fade_to(self, index: int):
        current = self.stack.currentWidget()

        effect = QGraphicsOpacityEffect(current)
        current.setGraphicsEffect(effect)

        fade_out = QPropertyAnimation(effect, b"opacity")
        fade_out.setDuration(150)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)

        def on_finished():
            self.stack.setCurrentIndex(index)

            new_widget = self.stack.currentWidget()

            effect_in = QGraphicsOpacityEffect(new_widget)
            new_widget.setGraphicsEffect(effect_in)
            effect_in.setOpacity(0.0)

            fade_in = QPropertyAnimation(effect_in, b"opacity")
            fade_in.setDuration(150)
            fade_in.setStartValue(0.0)
            fade_in.setEndValue(1.0)
            fade_in.start()

            # важно: сохранить ссылку
            self._last_animation = fade_in

        fade_out.finished.connect(on_finished)
        fade_out.start()

        # важно: сохранить ссылку
        self._last_animation = fade_out

    def resizeEvent(self, event):
        self.background.setGeometry(0, 0, self.window_width, self.window_height)
        self.overlay.setGeometry(0, 0, self.window_width, self.window_height)
