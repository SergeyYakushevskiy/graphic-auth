from PySide6.QtCore import Signal, Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtWidgets import QWidget

from src.domain.model import Point


class PasspointsCanvas(QWidget):
    point_added = Signal(QPoint)
    points_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._points: list[QPoint] = []
        self.ui_mask = []
        self._background = None

        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)


    def reset(self):
        self._points.clear()
        self.points_changed.emit(self._points)
        self.update()   # 🔥 важно

    def set_ui_rects(self, rects):
        self.ui_mask = rects

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        pos = event.position().toPoint()

        for r in self.ui_mask:
            if r.contains(pos):
                return

        point = event.position().toPoint()
        self._points.append(point)

        self.point_added.emit(point)
        self.points_changed.emit(self._points)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        if self._background:
            widget_rect = self.rect()
            pixmap = self._background

            scale = max(
                widget_rect.width() / pixmap.width(),
                widget_rect.height() / pixmap.height()
            )

            new_size = pixmap.size() * scale
            scaled_pixmap = pixmap.scaled(
                new_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            x = (widget_rect.width() - scaled_pixmap.width()) // 2
            y = (widget_rect.height() - scaled_pixmap.height()) // 2

            painter.drawPixmap(x, y, scaled_pixmap)

        for p in self._points:
            glow_color = QColor(90, 159, 212, 60)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(glow_color)
            painter.drawEllipse(p, 12, 12)

            mid_color = QColor(90, 159, 212, 180)
            painter.setBrush(mid_color)
            painter.drawEllipse(p, 7, 7)

            core_color = QColor(90, 159, 212)
            painter.setBrush(core_color)
            painter.drawEllipse(p, 3, 3)

    def set_background(self, pixmap: QPixmap):
        self._background = pixmap
        self.update()

    def get_points(self) -> list[Point]:
        return [self.qpoint_to_point(p) for p in self._points]

    def qpoint_to_point(self, p: QPoint) -> Point:
        return Point(x=float(p.x()), y=float(p.y()))