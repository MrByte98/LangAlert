"""
System Tray integration for LangAlert.
Draws dynamic vector icons and provides right-click context menu options.
"""
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QBrush, QPen, QLinearGradient, QPolygonF
from PyQt6.QtCore import Qt, pyqtSignal, QPointF

def create_tray_pixmap(is_active: bool = True, size: int = 64) -> QPixmap:
    """Generates a crisp high-DPI icon with the lightning bolt (⚡) logo and active status dot."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Outer rounded rectangle (Cyber Dark Base)
    bg_color = QColor("#0a0e1a")
    border_color = QColor("#00f0ff") if is_active else QColor("#475569")
    painter.setBrush(QBrush(bg_color))
    painter.setPen(QPen(border_color, 2.5))
    painter.drawRoundedRect(3, 3, size - 6, size - 6, 14, 14)

    # Lightning Bolt Polygon (⚡)
    poly = QPolygonF([
        QPointF(36, 10),  # Top tip
        QPointF(22, 33),  # Left middle
        QPointF(33, 33),  # Left waist
        QPointF(28, 54),  # Bottom tip
        QPointF(45, 28),  # Right middle
        QPointF(34, 28),  # Right waist
        QPointF(36, 10)   # Back to top
    ])

    if is_active:
        # Electric Cyan to Golden Yellow gradient
        grad = QLinearGradient(22, 10, 45, 54)
        grad.setColorAt(0.0, QColor("#00f0ff"))
        grad.setColorAt(0.5, QColor("#facc15"))
        grad.setColorAt(1.0, QColor("#ff9900"))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(255, 255, 255, 220), 1))
    else:
        painter.setBrush(QBrush(QColor("#64748b")))
        painter.setPen(QPen(QColor(148, 163, 184, 180), 1))

    painter.drawPolygon(poly)

    # Status indicator circle in bottom-right corner
    status_color = QColor("#10b981") if is_active else QColor("#ef4444")
    painter.setBrush(QBrush(status_color))
    painter.setPen(QPen(QColor("#0a0e1a"), 2))
    painter.drawEllipse(size - 18, size - 18, 14, 14)

    painter.end()
    return pixmap

class LangTrayIcon(QSystemTrayIcon):
    open_settings_requested = pyqtSignal()
    test_alert_requested = pyqtSignal()
    toggle_active_requested = pyqtSignal()
    quit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_active = True
        self.update_icon(True)
        self.setToolTip("LangAlert — دستیار زبان کیبورد")

        self._build_menu()
        self.activated.connect(self._on_activated)

    def _build_menu(self):
        menu = QMenu()
        menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.action_toggle = menu.addAction("⏸️ توقف موقت نظارت")
        self.action_toggle.triggered.connect(self.toggle_active_requested.emit)

        menu.addSeparator()

        action_test = menu.addAction("🔔 تست نمایش اعلان")
        action_test.triggered.connect(self.test_alert_requested.emit)

        action_settings = menu.addAction("⚙️ تنظیمات و تاریخچه")
        action_settings.triggered.connect(self.open_settings_requested.emit)

        menu.addSeparator()

        action_exit = menu.addAction("🚪 خروج کامل")
        action_exit.triggered.connect(self.quit_requested.emit)

        self.setContextMenu(menu)

    def update_icon(self, is_active: bool):
        self._is_active = is_active
        pixmap = create_tray_pixmap(is_active)
        self.setIcon(QIcon(pixmap))
        if hasattr(self, "action_toggle"):
            if is_active:
                self.action_toggle.setText("⏸️ توقف موقت نظارت")
            else:
                self.action_toggle.setText("▶️ ادامه نظارت")

    def _on_activated(self, reason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick
        ):
            self.open_settings_requested.emit()
