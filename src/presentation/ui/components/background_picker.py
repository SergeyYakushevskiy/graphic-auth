from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QPainterPath, QRegion, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLabel, QScrollArea, QHBoxLayout
)

from src.infrastructure.config.types import AppConfig
from src.presentation.ui.features.image_file import ImageTile


class BackgroundImagePicker(QWidget):
    """
    Pure selection component.
    Emits selected image path only.
    """

    image_selected = Signal(str)

    def __init__(self, config: AppConfig):
        super().__init__()

        self.config = config
        self.selected_path: str | None = None
        self.tiles: list[ImageTile] = []

        self._build()

    def _build(self):
        root = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollArea::viewport {
                background: transparent;
            }
        """)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ❌ УБРАНО центрирование через stretch
        # center_wrapper.addStretch()

        self.grid_container = QWidget()
        self.grid = QGridLayout(self.grid_container)

        # 👉 КЛЮЧЕВО: выравнивание влево-вверх
        self.grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.grid.setSpacing(10)
        self.grid.setContentsMargins(10, 10, 10, 10)

        container_layout.addWidget(self.grid_container)

        scroll.setWidget(container)

        root.addSpacing(10)
        root.addWidget(scroll)

        self._scroll = scroll

        self._load_images()

    def _load_images(self):
        images_dir = self.config.paths.assets_dir / "img" / "auth"

        images = sorted([
            p for p in images_dir.glob("*")
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
        ])

        for img in images:
            tile = ImageTile(img)
            tile.clicked.connect(self._on_selected)

            self.tiles.append(tile)
            self.grid.addWidget(tile, 0, 0)  # временно

        self._reflow_grid()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self._reflow_grid()
        self._apply_round_mask()

    def _apply_round_mask(self):
        rect = self.rect()

        path = QPainterPath()
        path.addRoundedRect(rect, 5, 5)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def _reflow_grid(self):
        if not self.tiles:
            return

        available_width = self._scroll.viewport().width()

        tile_w = 120
        spacing = self.grid.horizontalSpacing() or 10

        cols = max(1, available_width // (tile_w + spacing))

        # чистим grid
        items = []
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                items.append(item.widget())

        row, col = 0, 0

        for tile in items:
            self.grid.addWidget(tile, row, col)

            col += 1
            if col >= cols:
                col = 0
                row += 1

    def _on_selected(self, path: str):
        self.selected_path = path
        self.image_selected.emit(path)

        for tile in self.tiles:
            tile.set_selected(tile.image_path == Path(path))
