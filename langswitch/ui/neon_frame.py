"""
NeonFrame: Custom QFrame with anti-aliased cyan-to-purple gradient border
and soft glow shadow effect, matching the cyber glassmorphism design.
"""
from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen, QBrush

class NeonFrame(QFrame):
    def __init__(self, parent=None, radius=18, border_width=2):
        super().__init__(parent)
        self.radius = radius
        self.border_width = border_width

        # Soft glowing outer shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setColor(QColor(0, 240, 255, 60))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        half_bw = self.border_width / 2.0
        rect = self.rect().adjusted(
            int(half_bw) + 1, int(half_bw) + 1,
            -int(half_bw) - 1, -int(half_bw) - 1
        )

        # Translucent dark background
        painter.setBrush(QBrush(QColor(13, 17, 28, 235)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self.radius, self.radius)

        # Smooth gradient border (Cyan -> Sky Blue -> Violet/Magenta)
        gradient = QLinearGradient(0, 0, w, h)
        gradient.setColorAt(0.0, QColor("#00f0ff"))   # Cyan
        gradient.setColorAt(0.45, QColor("#38bdf8"))  # Sky
        gradient.setColorAt(0.85, QColor("#c084fc"))  # Violet
        gradient.setColorAt(1.0, QColor("#ec4899"))   # Magenta

        pen = QPen(QBrush(gradient), self.border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, self.radius, self.radius)
        painter.end()
