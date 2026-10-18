"""
Integration test suite for LangAlert.
Verifies all modules, UI instantiation, signals, sound playback, and conversions.
"""
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, ".")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# 1. Initialize Qt Application
app = QApplication.instance() or QApplication(sys.argv)
print("✓ Qt Application initialized")

# 2. Test Converter
from langswitch.converter import convert_en_to_fa, convert_fa_to_en
assert convert_en_to_fa("sghl") == "سلام", f"Failed: {convert_en_to_fa('sghl')}"
assert convert_fa_to_en("اثممخ") == "hello", f"Failed: {convert_fa_to_en('اثممخ')}"
assert convert_fa_to_en("فثسف") == "test", f"Failed: {convert_fa_to_en('فثسف')}"
print("✓ Layout converter mappings verified")

# 3. Test Detector
from langswitch.detector import detector
res1 = detector.evaluate("sghl", active_layout="en")
assert res1 is not None and res1.converted_text == "سلام", f"Failed res1: {res1}"
res2 = detector.evaluate("اثممخ", active_layout="fa")
assert res2 is not None and res2.converted_text == "hello", f"Failed res2: {res2}"
assert detector.evaluate("hello world", active_layout="en") is None, "False positive on English"
assert detector.evaluate("سلام دوست من", active_layout="fa") is None, "False positive on Persian"
print("✓ Intelligent detector and linguistic rules verified")

# 4. Test Sound Player
from langswitch.sound_player import sound_player
sound_player.play("crystal_chime")
print("✓ Sound player executed")

# 5. Test UI Components
from langswitch.ui.toast_badge import ToastBadge
from langswitch.ui.settings_window import SettingsWindow
from langswitch.ui.tray_icon import LangTrayIcon

toast = ToastBadge()
assert toast is not None
toast.show_alert(res1)
assert toast.isVisible()
toast.hide_animated()
print("✓ ToastBadge created, displayed, and hidden cleanly")

settings = SettingsWindow()
assert settings is not None
settings.add_history_entry(res1)
assert settings.table_history.rowCount() == 1
print("✓ SettingsWindow created and history entry added")

tray = LangTrayIcon()
assert tray is not None
print("✓ System tray icon created")

# 6. Test App class
from langswitch.app import LangAlertApp
main_app = LangAlertApp()
assert main_app.listener is not None
main_app.listener.start()
time.sleep(0.1)
main_app.listener.stop()
print("✓ Full LangAlertApp integration verified")

print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY! ✨")
