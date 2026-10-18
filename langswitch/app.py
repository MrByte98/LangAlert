"""
Main application coordinator for LangAlert.
Connects the keyboard listener, detection engine, tray icon, toast notifications,
and settings window into a coherent Qt application lifecycle.
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QFont

from .config import config
from .keyboard_listener import KeyboardListener
from .ui.toast_badge import ToastBadge
from .ui.settings_window import SettingsWindow
from .ui.tray_icon import LangTrayIcon

def load_vazir_fonts(app: QApplication):
    """Loads bundled Vazirmatn fonts and sets application default font."""
    font_dir = Path(__file__).parent / "fonts"
    for font_file in ["Vazirmatn-Regular.ttf", "Vazirmatn-Bold.ttf"]:
        p = font_dir / font_file
        if p.exists():
            QFontDatabase.addApplicationFont(str(p))

    app_font = QFont("Vazirmatn", 10)
    app_font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(app_font)

class LangAlertApp:
    def __init__(self):
        # Ensure QApplication exists
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.qt_app.setApplicationName("LangAlert")
        self.qt_app.setApplicationDisplayName("LangAlert — دستیار زبان کیبورد")
        self.qt_app.setQuitOnLastWindowClosed(False)

        # Load Vazir fonts
        load_vazir_fonts(self.qt_app)

        # Core services
        self.listener = KeyboardListener()
        self.toast = ToastBadge()
        self.settings_win = SettingsWindow()
        self.tray = LangTrayIcon()

        self._wire_signals()

    def _wire_signals(self):
        # 1. Keyboard detection -> Toast alert & History entry
        self.listener.mismatch_detected.connect(self._on_mismatch_detected)
        self.listener.status_changed.connect(self._on_listener_status_changed)

        # 2. Toast actions -> Listener text replacement
        self.toast.replace_requested.connect(self.listener.replace_text)

        # 3. Settings actions
        self.settings_win.test_alert_requested.connect(self.toast.show_alert)
        self.settings_win.status_toggled.connect(self.listener.set_active)
        self.settings_win.settings_changed.connect(self._on_settings_changed)

        # 4. Tray actions
        self.tray.open_settings_requested.connect(self.show_settings)
        self.tray.test_alert_requested.connect(self.settings_win._trigger_test_alert)
        self.tray.toggle_active_requested.connect(self.listener.toggle_active)
        self.tray.quit_requested.connect(self.quit)

    def _on_mismatch_detected(self, result):
        self.toast.show_alert(result)
        self.settings_win.add_history_entry(result)

    def _on_listener_status_changed(self, active: bool):
        self.tray.update_icon(active)
        self.settings_win._update_status_badge(active)

    def _on_settings_changed(self):
        self.settings_win.setWindowOpacity(config.get("window_opacity", 0.97))
        self.toast.setWindowOpacity(config.get("notification_opacity", 0.95))

    def show_settings(self):
        self.settings_win.show()
        self.settings_win.raise_()
        self.settings_win.activateWindow()

    def start(self, show_settings_on_start: bool = True):
        # Show tray icon
        self.tray.show()

        # Start keyboard hook
        self.listener.start()

        # Show notification or settings window
        if show_settings_on_start:
            self.show_settings()
        else:
            self.tray.showMessage(
                "LangAlert فعال شد",
                "دستیار اصلاح زبان کیبورد در پس‌زمینه در حال نظارت است.",
                self.tray.icon(),
                3000
            )

        # Run Qt Event Loop
        return self.qt_app.exec()

    def quit(self):
        self.listener.stop()
        self.tray.hide()
        self.toast.hide()
        self.settings_win.hide()
        self.qt_app.quit()
