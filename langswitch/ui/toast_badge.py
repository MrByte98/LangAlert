"""
Floating modern alert badge for LangAlert.
Matches the cyber glassmorphic style shown in the reference design.
"""
from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QGraphicsDropShadowEffect, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QCursor, QFont
import pyperclip

from ..config import config
from ..detector import DetectionResult
from ..sound_player import sound_player
from .styles import TOAST_CYBER_STYLESHEET

class ToastBadge(QWidget):
    # Signals
    replace_requested = pyqtSignal(str, str)  # (original, replacement)
    dismissed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_result: DetectionResult = None
        self._countdown_ms = 0
        self._total_duration_ms = 6000
        self._timer_interval_ms = 40
        self._is_paused = False

        self._setup_window_flags()
        self._init_ui()
        self._setup_timer()

    def _setup_window_flags(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setStyleSheet(TOAST_CYBER_STYLESHEET)

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(15, 15, 15, 15)

        # Main glassmorphism card
        self.card = QFrame()
        self.card.setObjectName("ToastMainFrame")
        self.setFixedWidth(350)

        # Outer soft glow shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 240, 255, 75))
        shadow.setOffset(0, 4)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(16, 14, 16, 12)
        card_layout.setSpacing(10)

        # --- Header row ---
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("CloseButton")
        self.btn_close.setFixedSize(24, 24)
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.clicked.connect(self.hide_animated)

        self.direction_badge = QLabel("EN ➔ FA")
        self.direction_badge.setObjectName("BadgeDirection")
        self.direction_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("زبان کیبورد اشتباه است!")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setFont(QFont("Vazirmatn", 13, QFont.Weight.Bold))
        self.title_label.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.icon_label = QLabel("⚡")
        self.icon_label.setObjectName("WarningIcon")
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header arrangement: Close on left, direction badge, title, warning icon on right
        header_layout.addWidget(self.btn_close)
        header_layout.addWidget(self.direction_badge)
        header_layout.addWidget(self.title_label, 1, Qt.AlignmentFlag.AlignRight)
        header_layout.addWidget(self.icon_label)
        card_layout.addLayout(header_layout)

        # --- Original text box ---
        self.orig_box = QFrame()
        self.orig_box.setObjectName("OriginalBox")
        orig_layout = QVBoxLayout(self.orig_box)
        orig_layout.setContentsMargins(10, 6, 10, 6)
        orig_layout.setSpacing(2)

        self.lbl_orig_title = QLabel("متن تایپ شده:")
        self.lbl_orig_title.setObjectName("OriginalLabel")
        self.lbl_orig_title.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.lbl_orig_val = QLabel("")
        self.lbl_orig_val.setObjectName("OriginalValue")
        self.lbl_orig_val.setWordWrap(True)

        orig_layout.addWidget(self.lbl_orig_title)
        orig_layout.addWidget(self.lbl_orig_val)
        card_layout.addWidget(self.orig_box)

        # --- Converted text box ---
        self.conv_box = QFrame()
        self.conv_box.setObjectName("ConvertedBox")
        conv_layout = QVBoxLayout(self.conv_box)
        conv_layout.setContentsMargins(10, 8, 10, 8)
        conv_layout.setSpacing(2)

        self.lbl_conv_title = QLabel("متن اصلاح شده (درست):")
        self.lbl_conv_title.setObjectName("ConvertedLabel")
        self.lbl_conv_title.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.lbl_conv_val = QLabel("")
        self.lbl_conv_val.setObjectName("ConvertedValue")
        self.lbl_conv_val.setFont(QFont("Vazirmatn", 15, QFont.Weight.Bold))
        self.lbl_conv_val.setWordWrap(True)

        conv_layout.addWidget(self.lbl_conv_title)
        conv_layout.addWidget(self.lbl_conv_val)
        card_layout.addWidget(self.conv_box)

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_copy = QPushButton("📋 کپی متن")
        self.btn_copy.setObjectName("CopyButton")
        self.btn_copy.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_copy.clicked.connect(self._on_copy_clicked)

        self.btn_replace = QPushButton("🔄 جایگزینی در متن")
        self.btn_replace.setObjectName("ReplaceButton")
        self.btn_replace.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_replace.clicked.connect(self._on_replace_clicked)

        # Layout order: Copy on left, Replace on right (or matching screenshot)
        btn_layout.addWidget(self.btn_copy, 1)
        btn_layout.addWidget(self.btn_replace, 1)
        card_layout.addLayout(btn_layout)

        # --- Progress countdown bar ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("CountdownBar")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        card_layout.addWidget(self.progress_bar)

        root_layout.addWidget(self.card)

    def _setup_timer(self):
        self._timer = QTimer(self)
        self._timer.setInterval(self._timer_interval_ms)
        self._timer.timeout.connect(self._on_timer_tick)

    def show_alert(self, result: DetectionResult):
        self._current_result = result
        
        self.lbl_orig_val.setText(result.original_text)
        self.lbl_conv_val.setText(result.converted_text)
        self.direction_badge.setText(result.direction_badge)

        if result.direction == "en_to_fa":
            self.lbl_conv_val.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.lbl_orig_val.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        else:
            self.lbl_conv_val.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.lbl_orig_val.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.btn_copy.setText("📋 کپی متن")

        # Play sound notification
        sound_player.play()

        # Position on screen
        self._position_on_screen()

        # Set user configured opacity
        opacity = config.get("notification_opacity", 0.96)
        self.setWindowOpacity(opacity)

        # Start countdown
        duration_sec = config.get("notification_duration_sec", 6)
        if duration_sec > 0:
            self._total_duration_ms = duration_sec * 1000
            self._countdown_ms = self._total_duration_ms
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(100)
            self._timer.start()
        else:
            self.progress_bar.setVisible(False)
            self._timer.stop()

        self.show()

    def _position_on_screen(self):
        screen = QApplication.primaryScreen()
        if not screen:
            return
        geo = screen.availableGeometry()

        pos_setting = config.get("notification_position", "top_right")
        margin_x = config.get("margin_x", 25)
        margin_y = config.get("margin_y", 45)

        self.adjustSize()
        w = self.width()
        h = self.height()

        if pos_setting == "top_left":
            x = geo.left() + margin_x
            y = geo.top() + margin_y
        elif pos_setting == "bottom_right":
            x = geo.right() - w - margin_x
            y = geo.bottom() - h - margin_y
        elif pos_setting == "bottom_left":
            x = geo.left() + margin_x
            y = geo.bottom() - h - margin_y
        else:  # "top_right"
            x = geo.right() - w - margin_x
            y = geo.top() + margin_y

        self.move(x, y)

    def _on_timer_tick(self):
        if self._is_paused:
            return

        self._countdown_ms -= self._timer_interval_ms
        if self._countdown_ms <= 0:
            self._timer.stop()
            self.hide_animated()
        else:
            pct = int((self._countdown_ms / self._total_duration_ms) * 100)
            self.progress_bar.setValue(pct)

    def _on_copy_clicked(self):
        if self._current_result:
            pyperclip.copy(self._current_result.converted_text)
            self.btn_copy.setText("کپی شد! ✓")
            QTimer.singleShot(1500, lambda: self.btn_copy.setText("📋 کپی متن"))

    def _on_replace_clicked(self):
        if self._current_result:
            orig = self._current_result.original_text
            conv = self._current_result.converted_text
            self.replace_requested.emit(orig, conv)
            self.hide_animated()

    def hide_animated(self):
        self._timer.stop()
        self.hide()
        self.dismissed.emit()

    def enterEvent(self, event):
        self._is_paused = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_paused = False
        super().leaveEvent(event)
