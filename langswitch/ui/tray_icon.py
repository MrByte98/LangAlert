"""
System Tray integration for LangAlert.
Draws dynamic vector icons and provides right-click context menu options.
"""
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QBrush, QPen
from PyQt6.QtCore import Qt, pyqtSignal

def create_tray_pixmap(is_active: bool = True, size: int = 64) -> QPixmap:
    """Generates a crisp high-DPI icon with keyboard symbol and active dot."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Outer rounded rectangle (keyboard body)
    bg_color = QColor("#0284c7") if is_active else QColor("#64748b")
    painter.setBrush(QBrush(bg_color))
    painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
    painter.drawRoundedRect(4, 8, size - 8, size - 16, 12, 12)

    # Key grid simulation
    painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
    painter.setPen(Qt.PenStyle.NoPen)
    
    # Draw mini keycaps
    key_size = 7
    gap = 4
    start_x = 12
    start_y = 18

    # Row 1
    for i in range(4):
        painter.drawRoundedRect(start_x + i * (key_size + gap), start_y, key_size, key_size, 2, 2)
    # Row 2
    for i in range(4):
        painter.drawRoundedRect(start_x + i * (key_size + gap), start_y + key_size + gap, key_size, key_size, 2, 2)
    # Spacebar
    painter.drawRoundedRect(start_x + 4, start_y + 2 * (key_size + gap), 26, 6, 2, 2)

    # Status indicator circle in corner
    status_color = QColor("#10b981") if is_active else QColor("#ef4444")
    painter.setBrush(QBrush(status_color))
    painter.setPen(QPen(QColor("#0f172a"), 2))
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
