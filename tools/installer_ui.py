"""
LangAlert Windows GUI Setup Installer.
Installs LangAlert.exe and shortcuts to user local application directory with ⚡ icon.
"""
import sys
import os
import shutil
import tempfile
import subprocess
import winreg
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QProgressBar, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QLinearGradient
from PyQt6.QtCore import Qt, QThread, pyqtSignal

APP_NAME = "LangAlert"
APP_DISPLAY_NAME = "⚡ LangAlert — دستیار زبان کیبورد"
VERSION = "1.0.0"
PUBLISHER = "MrByte98"

def create_windows_shortcut(target_path: Path, lnk_path: Path, icon_path: Path = None, description: str = ""):
    """Creates a Windows .lnk shortcut via WScript.Shell VBScript."""
    lnk_path.parent.mkdir(parents=True, exist_ok=True)
    vbs_content = f'''Set ws = CreateObject("WScript.Shell")
Set s = ws.CreateShortcut("{str(lnk_path)}")
s.TargetPath = "{str(target_path)}"
s.WorkingDirectory = "{str(target_path.parent)}"
s.Description = "{description}"
'''
    if icon_path and icon_path.exists():
        vbs_content += f's.IconLocation = "{str(icon_path)}, 0"\n'
    vbs_content += 's.Save\n'

    with tempfile.NamedTemporaryFile("w", suffix=".vbs", delete=False) as f:
        f.write(vbs_content)
        temp_vbs = f.name
    try:
        subprocess.run(["cscript", "//nologo", temp_vbs], check=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    finally:
        if os.path.exists(temp_vbs):
            os.remove(temp_vbs)

def register_uninstaller(install_dir: Path, target_exe: Path, icon_path: Path):
    """Registers LangAlert in Windows Add/Remove Programs (Registry)."""
    key_path = rf"Software\Microsoft\Windows\CurrentVersion\Uninstall\{APP_NAME}"
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_DISPLAY_NAME)
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, VERSION)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, PUBLISHER)
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, str(icon_path if icon_path.exists() else target_exe))
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(install_dir))
            
            # Create a simple uninstall batch script
            uninst_bat = install_dir / "uninstall.bat"
            desktop_lnk = Path.home() / "Desktop" / "LangAlert.lnk"
            start_menu_lnk = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "LangAlert.lnk"
            
            bat_script = f'''@echo off
taskkill /F /IM LangAlert.exe >nul 2>&1
del /F /Q "{str(desktop_lnk)}" >nul 2>&1
del /F /Q "{str(start_menu_lnk)}" >nul 2>&1
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" /f >nul 2>&1
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{APP_NAME}" /f >nul 2>&1
rmdir /S /Q "{str(install_dir)}" >nul 2>&1
echo LangAlert was uninstalled successfully.
'''
            with open(uninst_bat, "w", encoding="utf-8") as f:
                f.write(bat_script)
                
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'cmd.exe /c "{str(uninst_bat)}"')
    except Exception as e:
        print(f"Error registering uninstaller: {e}")

class InstallWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, create_desktop: bool, create_start: bool, autostart: bool):
        super().__init__()
        self.create_desktop = create_desktop
        self.create_start = create_start
        self.autostart = autostart

    def run(self):
        try:
            self.progress.emit(10, "در حال آماده‌سازی فایل‌های نصب...")
            
            # Source executable bundled or next to installer
            base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
            src_exe = base_dir / "LangAlert.exe"
            if not src_exe.exists():
                src_exe = base_dir / "dist" / "LangAlert.exe"
            if not src_exe.exists():
                src_exe = Path(__file__).resolve().parent.parent / "dist" / "LangAlert.exe"

            src_icon = base_dir / "assets" / "icon.ico"
            if not src_icon.exists():
                src_icon = Path(__file__).resolve().parent.parent / "assets" / "icon.ico"

            # Destination directory
            dest_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Programs" / APP_NAME
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_exe = dest_dir / "LangAlert.exe"
            dest_icon = dest_dir / "icon.ico"

            self.progress.emit(30, "در حال کپی و استقرار فایل‌های برنامه...")
            
            # Kill running instance if updating
            subprocess.run(["taskkill", "/F", "/IM", "LangAlert.exe"], capture_output=True)
            
            shutil.copy2(src_exe, dest_exe)
            if src_icon.exists():
                shutil.copy2(src_icon, dest_icon)

            self.progress.emit(60, "در حال ایجاد میانبرها و آیکون دسکتاپ...")
            if self.create_desktop:
                desktop_lnk = Path.home() / "Desktop" / "LangAlert.lnk"
                create_windows_shortcut(dest_exe, desktop_lnk, dest_icon, "LangAlert - دستیار زبان کیبورد")

            if self.create_start:
                start_menu_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
                start_lnk = start_menu_dir / "LangAlert.lnk"
                create_windows_shortcut(dest_exe, start_lnk, dest_icon, "LangAlert - دستیار زبان کیبورد")

            self.progress.emit(80, "در حال پیکربندی و ثبت در ویندوز...")
            register_uninstaller(dest_dir, dest_exe, dest_icon)

            if self.autostart:
                try:
                    run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_key, 0, winreg.KEY_SET_VALUE) as key:
                        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{str(dest_exe)}" --minimized')
                except Exception as e:
                    print(f"Error setting autostart: {e}")

            self.progress.emit(100, "نصب با موفقیت به پایان رسید!")
            self.finished.emit(True, str(dest_exe))

        except Exception as e:
            self.finished.emit(False, str(e))

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نصب دستیار زبان کیبورد LangAlert ⚡")
        self.resize(520, 420)
        self.setFixedSize(520, 420)

        # Apply dark cyber glass theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e1a;
            }
            QWidget {
                color: #f1f5f9;
                font-family: 'Segoe UI', Tahoma, sans-serif;
            }
            QCheckBox {
                font-size: 13px;
                color: #cbd5e1;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid rgba(0, 240, 255, 0.4);
                background-color: rgba(15, 23, 42, 0.8);
            }
            QCheckBox::indicator:checked {
                background-color: #00f0ff;
                image: none;
            }
            QProgressBar {
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                text-align: center;
                background-color: rgba(15, 23, 42, 0.8);
                color: #f8fafc;
                font-weight: bold;
                height: 22px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f0ff, stop:1 #a855f7);
                border-radius: 7px;
            }
        """)

        # Set Window Icon
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
        icon_path = base_dir / "assets" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Header with ⚡ Logo
        header = QHBoxLayout()
        logo_lbl = QLabel("⚡")
        logo_lbl.setStyleSheet("""
            font-size: 32px;
            color: #facc15;
            background-color: rgba(0, 240, 255, 0.15);
            border: 1px solid rgba(0, 240, 255, 0.4);
            border-radius: 24px;
            padding: 4px 10px;
        """)
        
        title_box = QVBoxLayout()
        title_lbl = QLabel("LangAlert Setup")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #00f0ff;")
        desc_lbl = QLabel("دستیار هوشمند تصحیح زبان کیبورد (فارسی ⮂ انگلیسی)")
        desc_lbl.setStyleSheet("font-size: 12px; color: #94a3b8;")
        title_box.addWidget(title_lbl)
        title_box.addWidget(desc_lbl)

        header.addWidget(logo_lbl)
        header.addLayout(title_box)
        header.addStretch()
        layout.addLayout(header)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); max-height: 1px;")
        layout.addWidget(line)

        # Install options
        layout.addSpacing(6)
        opts_title = QLabel("گزینه‌های نصب:")
        opts_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #e2e8f0;")
        layout.addWidget(opts_title)

        self.chk_desktop = QCheckBox("ایجاد آیکون و میانبر روی دسکتاپ (Desktop Shortcut)")
        self.chk_desktop.setChecked(True)
        self.chk_desktop.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        layout.addWidget(self.chk_desktop)

        self.chk_start = QCheckBox("ایجاد میانبر در منوی استارت (Start Menu)")
        self.chk_start.setChecked(True)
        self.chk_start.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        layout.addWidget(self.chk_start)

        self.chk_autostart = QCheckBox("اجرای خودکار هنگام بالا آمدن ویندوز (Windows Startup)")
        self.chk_autostart.setChecked(True)
        self.chk_autostart.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        layout.addWidget(self.chk_autostart)

        layout.addSpacing(10)

        # Progress bar
        self.prog_bar = QProgressBar()
        self.prog_bar.setRange(0, 100)
        self.prog_bar.setValue(0)
        self.prog_bar.setVisible(False)
        layout.addWidget(self.prog_bar)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("font-size: 12px; color: #38bdf8;")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_lbl)

        layout.addStretch()

        # Action Button
        self.btn_install = QPushButton("🚀 نصب سریع LangAlert")
        self.btn_install.setFixedHeight(44)
        self.btn_install.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f0ff, stop:1 #a855f7);
                color: #041a2e;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #c084fc);
            }
        """)
        self.btn_install.clicked.connect(self._start_install)
        layout.addWidget(self.btn_install)

    def _start_install(self):
        self.btn_install.setEnabled(False)
        self.prog_bar.setVisible(True)
        self.worker = InstallWorker(
            create_desktop=self.chk_desktop.isChecked(),
            create_start=self.chk_start.isChecked(),
            autostart=self.chk_autostart.isChecked()
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, val: int, msg: str):
        self.prog_bar.setValue(val)
        self.status_lbl.setText(msg)

    def _on_finished(self, success: bool, res: str):
        if success:
            self.status_lbl.setText("✅ برنامه با موفقیت نصب شد! در حال اجرای برنامه...")
            # Launch installed LangAlert.exe
            try:
                subprocess.Popen([res])
            except Exception as e:
                print(f"Error launching: {e}")
            QMessageBox.information(
                self,
                "نصب موفقیت‌آمیز ⚡",
                "برنامه LangAlert با موفقیت روی سیستم شما نصب شد و در نوار وظیفه (System Tray) به صورت فعال شروع به کار کرد!"
            )
            self.close()
        else:
            QMessageBox.critical(self, "خطا در نصب", f"خطایی در فرآیند نصب رخ داد:\n{res}")
            self.btn_install.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    win = InstallerWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
