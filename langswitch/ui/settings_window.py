"""
Modern Cyber Neon Settings & Dashboard Window for LangAlert.
Matches the exact glowing cyan/purple aesthetic with Vazirmatn Persian typography
and real-time Opacity controls.
"""
from datetime import datetime
from pathlib import Path
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QCheckBox, QSlider, QComboBox,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QColor, QIcon
import pyperclip

from ..config import config
from ..converter import convert_en_to_fa, convert_fa_to_en
from ..detector import detector, DetectionResult
from ..sound_player import sound_player
from .styles import CYBER_DARK_THEME
from .neon_frame import NeonFrame

class SettingsWindow(QMainWindow):
    # Signals
    test_alert_requested = pyqtSignal(object)  # Emits DetectionResult
    settings_changed = pyqtSignal()
    status_toggled = pyqtSignal(bool)

    def __init__(self, history_manager=None, parent=None):
        super().__init__(parent)
        self.history_manager = history_manager or []
        self.setWindowTitle("⚡ LangAlert — تنظیمات و مدیریت دستیار زبان کیبورد")
        self.resize(780, 640)
        self.setMinimumSize(700, 580)
        
        # Set icon
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
        icon_path = base_dir / "assets" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        self.setStyleSheet(CYBER_DARK_THEME)
        self._init_ui()
        self._load_values()

        # Apply initial window opacity
        win_op = config.get("window_opacity", 0.97)
        self.setWindowOpacity(win_op)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 16, 20, 18)
        main_layout.setSpacing(12)

        # Header Title & Live Status Indicator
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(4, 0, 4, 0)

        header_title = QLabel("⚡ LangAlert — دستیار هوشمند زبان کیبورد")
        header_title.setFont(QFont("Vazirmatn", 15, QFont.Weight.Bold))
        header_title.setStyleSheet("color: #f8fafc;")
        header_title.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.lbl_status_badge = QLabel("● فعال")
        self.lbl_status_badge.setFont(QFont("Vazirmatn", 13, QFont.Weight.Bold))
        self.lbl_status_badge.setStyleSheet("color: #10b981; font-weight: bold; font-size: 13px;")
        badge_glow = QGraphicsDropShadowEffect(self)
        badge_glow.setBlurRadius(10)
        badge_glow.setColor(QColor("#10b981"))
        badge_glow.setOffset(0, 0)
        self.lbl_status_badge.setGraphicsEffect(badge_glow)

        header_layout.addWidget(header_title)
        header_layout.addStretch()
        header_layout.addWidget(self.lbl_status_badge)
        main_layout.addLayout(header_layout)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.tab_detection = QWidget()
        self.tab_history_ui = QWidget()
        self.tab_playground = QWidget()
        self.tab_about = QWidget()

        # Right-to-Left tab ordering matching user reference
        self.tabs.addTab(self.tab_detection, "⚙️ تنظیمات تشخیص")
        self.tabs.addTab(self.tab_history_ui, "🎨 📋 تاریخچه و ظاهر")
        self.tabs.addTab(self.tab_playground, "⚡ تست زنده")
        self.tabs.addTab(self.tab_about, "ℹ️ راهنما و درباره")

        self._build_detection_tab()
        self._build_history_ui_tab()
        self._build_playground_tab()
        self._build_about_tab()

        main_layout.addWidget(self.tabs, 1)

        # Footer Buttons matching screenshot: Test Alert (left), Reset (center), Save (right)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(4, 8, 4, 0)
        footer_layout.setSpacing(12)

        self.btn_test = QPushButton("🔔 تست اعلان در صفحه")
        self.btn_test.setProperty("class", "btnTestAlert")
        self.btn_test.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_test.clicked.connect(self._trigger_test_alert)

        self.btn_reset = QPushButton("بازگردانی به پیش‌فرض")
        self.btn_reset.setProperty("class", "btnReset")
        self.btn_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_reset.clicked.connect(self._reset_defaults)

        self.btn_save = QPushButton("ذخیره و اعمال تنظیمات")
        self.btn_save.setProperty("class", "btnSave")
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.clicked.connect(self._save_values)

        footer_layout.addWidget(self.btn_test)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_reset)
        footer_layout.addWidget(self.btn_save)
        main_layout.addLayout(footer_layout)

    # ------------------ Detection Tab ------------------
    def _build_detection_tab(self):
        tab_layout = QVBoxLayout(self.tab_detection)
        tab_layout.setContentsMargins(0, 8, 0, 0)

        # Glowing Neon Frame Container
        self.neon_container = NeonFrame(radius=18, border_width=2)
        neon_layout = QVBoxLayout(self.neon_container)
        neon_layout.setContentsMargins(16, 16, 16, 16)
        neon_layout.setSpacing(12)

        # Card 1: Master enable checkbox
        card_master = QFrame()
        card_master.setProperty("class", "innerCard")
        cm_layout = QVBoxLayout(card_master)
        cm_layout.setContentsMargins(14, 12, 14, 12)
        
        self.chk_enabled = QCheckBox("نظارت خودکار روی کلیدهای تایپ شده فعال باشد")
        self.chk_enabled.setFont(QFont("Vazirmatn", 12, QFont.Weight.Bold))
        self.chk_enabled.toggled.connect(self._on_master_toggle)
        cm_layout.addWidget(self.chk_enabled)
        neon_layout.addWidget(card_master)

        # Card 2: Direction options
        card_dirs = QFrame()
        card_dirs.setProperty("class", "innerCard")
        cd_layout = QVBoxLayout(card_dirs)
        cd_layout.setContentsMargins(14, 12, 14, 12)
        cd_layout.setSpacing(8)
        
        lbl_dirs = QLabel("جهت‌های تشخیص اشتباه زبان:")
        lbl_dirs.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        lbl_dirs.setStyleSheet("color: #f1f5f9;")
        cd_layout.addWidget(lbl_dirs)

        self.chk_en_to_fa = QCheckBox("تشخیص انگلیسی به فارسی (کیبورد انگلیسی بوده اما قصد تایپ فارسی بوده - مثل sghl ➔ سلام)")
        self.chk_en_to_fa.setFont(QFont("Vazirmatn", 11))

        self.chk_fa_to_en = QCheckBox("تشخیص فارسی به انگلیسی (کیبورد فارسی بوده اما قصد انگلیسی بوده - مثل اثممخ ➔ hello)")
        self.chk_fa_to_en.setFont(QFont("Vazirmatn", 11))

        cd_layout.addWidget(self.chk_en_to_fa)
        cd_layout.addWidget(self.chk_fa_to_en)
        neon_layout.addWidget(card_dirs)

        # Card 3: Sliders & Triggers
        card_params = QFrame()
        card_params.setProperty("class", "innerCard")
        cp_layout = QGridLayout(card_params)
        cp_layout.setContentsMargins(14, 14, 14, 14)
        cp_layout.setHorizontalSpacing(14)
        cp_layout.setVerticalSpacing(8)

        # Timeout Slider
        lbl_timeout_title = QLabel("زمان بررسی پس از مکث در (تایم‌اوت):")
        lbl_timeout_title.setFont(QFont("Vazirmatn", 11))
        
        self.lbl_timeout_val = QLabel("1000 میلی‌ثانیه")
        self.lbl_timeout_val.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.lbl_timeout_val.setStyleSheet("color: #00f0ff;")
        self.lbl_timeout_val.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.slider_timeout = QSlider(Qt.Orientation.Horizontal)
        self.slider_timeout.setRange(300, 3000)
        self.slider_timeout.setSingleStep(100)
        self.slider_timeout.setValue(1000)
        self.slider_timeout.valueChanged.connect(
            lambda v: self.lbl_timeout_val.setText(f"{v} میلی‌ثانیه")
        )

        cp_layout.addWidget(lbl_timeout_title, 0, 1)
        cp_layout.addWidget(self.lbl_timeout_val, 0, 0)
        cp_layout.addWidget(self.slider_timeout, 1, 0, 1, 2)

        # Min Word Length Slider
        lbl_minlen_title = QLabel("حداقل طول کلمه برای بررسی:")
        lbl_minlen_title.setFont(QFont("Vazirmatn", 11))

        self.lbl_minlen_val = QLabel("3 کاراکتر")
        self.lbl_minlen_val.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.lbl_minlen_val.setStyleSheet("color: #00f0ff;")
        self.lbl_minlen_val.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.slider_minlen = QSlider(Qt.Orientation.Horizontal)
        self.slider_minlen.setRange(2, 6)
        self.slider_minlen.setValue(3)
        self.slider_minlen.valueChanged.connect(
            lambda v: self.lbl_minlen_val.setText(f"{v} کاراکتر")
        )

        cp_layout.addWidget(lbl_minlen_title, 2, 1)
        cp_layout.addWidget(self.lbl_minlen_val, 2, 0)
        cp_layout.addWidget(self.slider_minlen, 3, 0, 1, 2)

        # Trigger Checkboxes in two columns
        self.chk_trig_space = QCheckBox("بررسی با زدن کلید Space")
        self.chk_trig_space.setFont(QFont("Vazirmatn", 11))

        self.chk_trig_enter = QCheckBox("بررسی با زدن کلید Enter")
        self.chk_trig_enter.setFont(QFont("Vazirmatn", 11))

        self.chk_trig_pause = QCheckBox("بررسی خودکار هنگام مکث در تایپ (تایم‌اوت)")
        self.chk_trig_pause.setFont(QFont("Vazirmatn", 11))

        cp_layout.addWidget(self.chk_trig_space, 4, 1)
        cp_layout.addWidget(self.chk_trig_enter, 4, 0)
        cp_layout.addWidget(self.chk_trig_pause, 5, 0, 1, 2)

        neon_layout.addWidget(card_params)
        tab_layout.addWidget(self.neon_container)

    # ------------------ History & Appearance Tab ------------------
    def _build_history_ui_tab(self):
        layout = QVBoxLayout(self.tab_history_ui)
        layout.setContentsMargins(8, 12, 8, 8)
        layout.setSpacing(12)

        # Card: Opacity Controls (Real-time live adjustment)
        card_opacity = QFrame()
        card_opacity.setProperty("class", "innerCard")
        co_layout = QGridLayout(card_opacity)
        co_layout.setContentsMargins(14, 12, 14, 12)
        co_layout.setHorizontalSpacing(14)
        co_layout.setVerticalSpacing(8)

        # Window Opacity Slider
        lbl_win_op_title = QLabel("شفافیت پنجره برنامه (Window Opacity):")
        lbl_win_op_title.setFont(QFont("Vazirmatn", 11))

        self.lbl_win_op_val = QLabel("97%")
        self.lbl_win_op_val.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.lbl_win_op_val.setStyleSheet("color: #00f0ff;")

        self.slider_win_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_win_opacity.setRange(50, 100)
        self.slider_win_opacity.setValue(97)
        self.slider_win_opacity.valueChanged.connect(self._on_window_opacity_changed)

        co_layout.addWidget(lbl_win_op_title, 0, 1)
        co_layout.addWidget(self.lbl_win_op_val, 0, 0)
        co_layout.addWidget(self.slider_win_opacity, 1, 0, 1, 2)

        # Toast Opacity Slider
        lbl_toast_op_title = QLabel("شفافیت بج اعلان شناور (Notification Opacity):")
        lbl_toast_op_title.setFont(QFont("Vazirmatn", 11))

        self.lbl_toast_op_val = QLabel("95%")
        self.lbl_toast_op_val.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        self.lbl_toast_op_val.setStyleSheet("color: #00f0ff;")

        self.slider_toast_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_toast_opacity.setRange(50, 100)
        self.slider_toast_opacity.setValue(95)
        self.slider_toast_opacity.valueChanged.connect(
            lambda v: self.lbl_toast_op_val.setText(f"{v}%")
        )

        co_layout.addWidget(lbl_toast_op_title, 2, 1)
        co_layout.addWidget(self.lbl_toast_op_val, 2, 0)
        co_layout.addWidget(self.slider_toast_opacity, 3, 0, 1, 2)

        layout.addWidget(card_opacity)

        # History Table
        lbl_history_title = QLabel("تاریخچه کلمات تصحیح‌شده (برای کپی سریع دوبار کلیک کنید):")
        lbl_history_title.setFont(QFont("Vazirmatn", 11, QFont.Weight.Bold))
        layout.addWidget(lbl_history_title)

        self.table_history = QTableWidget()
        self.table_history.setColumnCount(4)
        self.table_history.setHorizontalHeaderLabels(["زمان", "جهت", "متن اولیه", "متن اصلاح شده"])
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_history.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_history.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_history.doubleClicked.connect(self._on_history_row_double_clicked)
        layout.addWidget(self.table_history, 1)

    # ------------------ Playground Tab ------------------
    def _build_playground_tab(self):
        layout = QVBoxLayout(self.tab_playground)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(12)

        lbl_desc = QLabel(
            "در این بخش می‌توانید کلماتی مانند «sghl» یا «اثممخ» را تایپ کنید "
            "تا نحوه عملکرد موتور هوشمند را به صورت زنده مشاهده کنید:"
        )
        lbl_desc.setWordWrap(True)
        layout.addWidget(lbl_desc)

        self.txt_play_input = QLineEdit()
        self.txt_play_input.setPlaceholderText("اینجا تایپ کنید... مثلاً sghl یا اثممخ یا o,fd")
        self.txt_play_input.textChanged.connect(self._on_playground_text_changed)
        layout.addWidget(self.txt_play_input)

        card_result = QFrame()
        card_result.setProperty("class", "innerCard")
        cr_layout = QVBoxLayout(card_result)
        cr_layout.setContentsMargins(14, 14, 14, 14)

        self.lbl_play_result_status = QLabel("نتیجه بررسی: متنی وارد نشده است.")
        self.lbl_play_result_status.setStyleSheet("color: #94a3b8; font-weight: bold;")

        self.lbl_play_converted = QLabel("")
        self.lbl_play_converted.setFont(QFont("Vazirmatn", 16, QFont.Weight.Bold))
        self.lbl_play_converted.setStyleSheet("color: #10b981;")

        self.lbl_play_reason = QLabel("")
        self.lbl_play_reason.setStyleSheet("color: #cbd5e1; font-size: 12px;")
        self.lbl_play_reason.setWordWrap(True)

        cr_layout.addWidget(self.lbl_play_result_status)
        cr_layout.addWidget(self.lbl_play_converted)
        cr_layout.addWidget(self.lbl_play_reason)
        layout.addWidget(card_result)

        btn_row = QHBoxLayout()
        self.btn_play_trigger_alert = QPushButton("🔔 شبیه‌سازی نمایش هشدار گوشه صفحه با این متن")
        self.btn_play_trigger_alert.setProperty("class", "btnTestAlert")
        self.btn_play_trigger_alert.clicked.connect(self._trigger_playground_alert)

        btn_row.addWidget(self.btn_play_trigger_alert)
        btn_row.addStretch()
        layout.addLayout(btn_row)
        layout.addStretch()

    # ------------------ About Tab ------------------
    def _build_about_tab(self):
        layout = QVBoxLayout(self.tab_about)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        lbl_app_title = QLabel("LangAlert v1.0.0")
        lbl_app_title.setFont(QFont("Vazirmatn", 18, QFont.Weight.Bold))
        lbl_app_title.setStyleSheet("color: #00f0ff;")
        layout.addWidget(lbl_app_title)

        lbl_about_text = QLabel(
            "<b>دستیار هوشمند تصحیح خطای زبان کیبورد</b><br><br>"
            "این نرم‌افزار به صورت یک سرویس سبک در پس‌زمینه سیستم‌عامل (System Tray) اجرا می‌شود "
            "و زمانی که کاربر بدون توجه به زبان ست‌شده، متنی را به اشتباه با چیدمان زبان دوم تایپ کند، "
            "با یک صدای مشخص و یک بج اعلان شیک در گوشه صفحه هشدار می‌دهد.<br><br>"
            "<b>طراحی و قالب:</b> قالب شیشه‌ای Cyber Neon به همراه فونت زیبای <b>وزیر (Vazirmatn)</b>."
        )
        lbl_about_text.setWordWrap(True)
        lbl_about_text.setStyleSheet("line-height: 1.7; color: #cbd5e1;")
        layout.addWidget(lbl_about_text)
        layout.addStretch()

    # ------------------ Logic & Actions ------------------
    def _load_values(self):
        self.chk_enabled.setChecked(config.get("enabled", True))
        self.chk_en_to_fa.setChecked(config.get("check_en_to_fa", True))
        self.chk_fa_to_en.setChecked(config.get("check_fa_to_en", True))
        
        timeout_val = config.get("detection_timeout_ms", 1000)
        self.slider_timeout.setValue(timeout_val)
        self.lbl_timeout_val.setText(f"{timeout_val} میلی‌ثانیه")

        minlen_val = config.get("min_word_length", 3)
        self.slider_minlen.setValue(minlen_val)
        self.lbl_minlen_val.setText(f"{minlen_val} کاراکتر")

        self.chk_trig_space.setChecked(config.get("trigger_on_space", True))
        self.chk_trig_enter.setChecked(config.get("trigger_on_enter", True))
        self.chk_trig_pause.setChecked(config.get("trigger_on_pause", True))

        # Opacities
        win_op = int(config.get("window_opacity", 0.97) * 100)
        self.slider_win_opacity.setValue(win_op)
        self.lbl_win_op_val.setText(f"{win_op}%")

        toast_op = int(config.get("notification_opacity", 0.95) * 100)
        self.slider_toast_opacity.setValue(toast_op)
        self.lbl_toast_op_val.setText(f"{toast_op}%")

    def _save_values(self):
        config.set("enabled", self.chk_enabled.isChecked())
        config.set("check_en_to_fa", self.chk_en_to_fa.isChecked())
        config.set("check_fa_to_en", self.chk_fa_to_en.isChecked())
        config.set("detection_timeout_ms", self.slider_timeout.value())
        config.set("min_word_length", self.slider_minlen.value())
        config.set("trigger_on_space", self.chk_trig_space.isChecked())
        config.set("trigger_on_enter", self.chk_trig_enter.isChecked())
        config.set("trigger_on_pause", self.chk_trig_pause.isChecked())

        config.set("window_opacity", self.slider_win_opacity.value() / 100.0)
        config.set("notification_opacity", self.slider_toast_opacity.value() / 100.0)

        self._update_status_badge(self.chk_enabled.isChecked())
        self.settings_changed.emit()

        QMessageBox.information(self, "تنظیمات", "تنظیمات با موفقیت ذخیره و اعمال شد.")

    def _reset_defaults(self):
        reply = QMessageBox.question(
            self, "بازنشانی",
            "آیا مایلید تمام تنظیمات به حالت پیش‌فرض اولیه بازگردند؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            config.reset_to_defaults()
            self._load_values()
            self.settings_changed.emit()

    def _on_window_opacity_changed(self, value: int):
        self.lbl_win_op_val.setText(f"{value}%")
        # Live opacity preview on current window
        self.setWindowOpacity(value / 100.0)

    def _on_master_toggle(self, enabled: bool):
        self._update_status_badge(enabled)
        self.status_toggled.emit(enabled)

    def _update_status_badge(self, active: bool):
        if active:
            self.lbl_status_badge.setText("● فعال")
            self.lbl_status_badge.setStyleSheet("color: #10b981; font-weight: bold; font-size: 13px;")
        else:
            self.lbl_status_badge.setText("○ متوقف شده")
            self.lbl_status_badge.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 13px;")

    def _trigger_test_alert(self):
        sample = DetectionResult(
            original_text="sghl xxhvd",
            converted_text="سلام چطوری",
            direction="en_to_fa",
            confidence=0.99,
            reason="تست اعلان نمونه - کیبورد روی انگلیسی تنظیم شده بود.",
            matched_words=["سلام", "چطوری"]
        )
        self.test_alert_requested.emit(sample)

    def _on_playground_text_changed(self, text: str):
        text = text.strip()
        if not text:
            self.lbl_play_result_status.setText("نتیجه بررسی: متنی وارد نشده است.")
            self.lbl_play_result_status.setStyleSheet("color: #94a3b8; font-weight: bold;")
            self.lbl_play_converted.setText("")
            self.lbl_play_reason.setText("")
            return

        res = detector.evaluate(text)
        if res:
            self.lbl_play_result_status.setText(f"✓ اشتباه در تایپ تشخیص داده شد! ({res.direction_label})")
            self.lbl_play_result_status.setStyleSheet("color: #f59e0b; font-weight: bold;")
            self.lbl_play_converted.setText(res.converted_text)
            self.lbl_play_reason.setText(res.reason)
        else:
            self.lbl_play_result_status.setText("متن وارد شده مطابق زبان صحیح است یا خطایی یافت نشد.")
            self.lbl_play_result_status.setStyleSheet("color: #10b981; font-weight: bold;")
            self.lbl_play_converted.setText("")
            self.lbl_play_reason.setText("")

    def _trigger_playground_alert(self):
        text = self.txt_play_input.text().strip() or "sghl xxhvd"
        res = detector.evaluate(text)
        if not res:
            conv = convert_en_to_fa(text) if text.isascii() else convert_fa_to_en(text)
            direction = "en_to_fa" if text.isascii() else "fa_to_en"
            res = DetectionResult(
                original_text=text,
                converted_text=conv,
                direction=direction,
                confidence=0.95,
                reason="شبیه‌سازی دستی از محیط تست زنده",
                matched_words=[conv]
            )
        self.test_alert_requested.emit(res)

    def add_history_entry(self, result: DetectionResult):
        time_str = datetime.now().strftime("%H:%M:%S")
        self.table_history.insertRow(0)
        self.table_history.setItem(0, 0, QTableWidgetItem(time_str))
        self.table_history.setItem(0, 1, QTableWidgetItem(result.direction_badge))
        self.table_history.setItem(0, 2, QTableWidgetItem(result.original_text))
        self.table_history.setItem(0, 3, QTableWidgetItem(result.converted_text))

    def _on_history_row_double_clicked(self, index):
        row = index.row()
        item = self.table_history.item(row, 3)
        if item:
            pyperclip.copy(item.text())
            QMessageBox.information(self, "کپی", f"متن اصلاح شده کپی شد:\n{item.text()}")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
