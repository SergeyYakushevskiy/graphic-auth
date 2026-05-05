from pathlib import Path

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QPainterPath, QRegion
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class ImageTile(QFrame):
    clicked = Signal(str)

    def __init__(self, image_path: Path):
        super().__init__()

        self.image_path = image_path
        self._selected = False

        self._build()

    def _build(self):
        self.setFixedSize(120, 90)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self.label = QLabel(self)

        pix = QPixmap(str(self.image_path)).scaled(
            116,
            86,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(pix)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label)

        self.setStyleSheet(self._style(False))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_round_mask()

    def _apply_round_mask(self):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 8, 8)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        self.clicked.emit(str(self.image_path))

    def set_selected(self, value: bool):
        self._selected = value
        self.setStyleSheet(self._style(value))

    def _style(self, selected: bool) -> str:
        if selected:
            return """
                QFrame {
                    border: 2px solid #5A9FD4;
                    border-radius: 8px;
                    background-color: rgba(90, 159, 212, 0.15);
                }
            """
        return """
            QFrame {
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                background-color: rgba(25, 25, 25, 0.5);
            }

            QFrame:hover {
                border: 1px solid rgba(90, 159, 212, 0.5);
            }
        """
