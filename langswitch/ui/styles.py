"""
Cyber Neon Glassmorphism Theme for LangAlert.
Matches the exact glowing cyan/purple aesthetic with Vazirmatn Persian typography.
"""

FONT_FAMILY = "'Vazirmatn', 'Vazir', 'Segoe UI', Tahoma, -apple-system, sans-serif"

CYBER_DARK_THEME = f"""
QWidget {{
    font-family: {FONT_FAMILY};
    color: #f1f5f9;
    font-size: 13px;
}}

QMainWindow, QDialog {{
    background-color: #0a0e1a;
}}

/* Tab Widget Container */
QTabWidget::pane {{
    border: none;
    background-color: transparent;
    top: 6px;
}}

QTabBar {{
    background: transparent;
    qproperty-drawBase: 0;
}}

QTabBar::tab {{
    background-color: rgba(30, 41, 59, 0.65);
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 8px 18px;
    margin-left: 6px;
    margin-right: 6px;
    font-weight: 600;
    font-size: 13px;
}}

QTabBar::tab:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f0ff, stop:1 #06b6d4);
    color: #041a2e;
    border: 1px solid #38bdf8;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: rgba(51, 65, 85, 0.8);
    color: #ffffff;
    border-color: rgba(0, 240, 255, 0.4);
}}

/* Inner Section Cards */
QFrame.innerCard {{
    background-color: rgba(18, 24, 38, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
}}

QFrame.innerCard:hover {{
    border-color: rgba(0, 240, 255, 0.35);
}}

/* Checkboxes */
QCheckBox {{
    spacing: 10px;
    font-size: 13px;
    color: #f8fafc;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid rgba(148, 163, 184, 0.6);
    border-radius: 5px;
    background-color: rgba(15, 23, 42, 0.6);
}}

QCheckBox::indicator:hover {{
    border-color: #00f0ff;
}}

QCheckBox::indicator:checked {{
    background-color: #00e5ff;
    border-color: #00f0ff;
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23082f49' stroke-width='3.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'></polyline></svg>");
}}

/* Sliders */
QSlider::groove:horizontal {{
    height: 6px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f0ff, stop:1 #38bdf8);
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: #ffffff;
    border: 3px solid #00f0ff;
    width: 18px;
    height: 18px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: #00f0ff;
    border-color: #ffffff;
}}

/* Action Buttons */
QPushButton.btnSave {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d2ff, stop:1 #0284c7);
    color: #ffffff;
    border: 1px solid #38bdf8;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: bold;
    font-size: 13px;
}}

QPushButton.btnSave:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #0369a1);
    border-color: #7dd3fc;
}}

QPushButton.btnReset {{
    background-color: rgba(51, 65, 85, 0.85);
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: bold;
    font-size: 13px;
}}

QPushButton.btnReset:hover {{
    background-color: rgba(71, 85, 105, 0.95);
    border-color: rgba(255, 255, 255, 0.35);
}}

QPushButton.btnTestAlert {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
    color: #ffffff;
    border: 1px solid #34d399;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: bold;
    font-size: 13px;
}}

QPushButton.btnTestAlert:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34d399, stop:1 #10b981);
    border-color: #6ee7b7;
}}

/* Form elements */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {{
    background-color: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 8px 12px;
    color: #f8fafc;
    selection-background-color: #0284c7;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border-color: #00f0ff;
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: #1e293b;
    border: 1px solid #334155;
    selection-background-color: #0284c7;
    color: #f8fafc;
    border-radius: 8px;
    padding: 4px;
}}

/* Table Widget */
QTableWidget {{
    background-color: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    gridline-color: rgba(255, 255, 255, 0.08);
}}

QHeaderView::section {{
    background-color: #1e293b;
    color: #94a3b8;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #334155;
    font-weight: 600;
}}
"""

TOAST_CYBER_STYLESHEET = f"""
QFrame#ToastMainFrame {{
    background-color: rgba(13, 17, 28, 0.96);
    border: 1px solid rgba(0, 240, 255, 0.35);
    border-radius: 18px;
}}

QLabel#TitleLabel {{
    color: #f8fafc;
    font-weight: 700;
    font-size: 14px;
}}

QLabel#BadgeDirection {{
    background-color: rgba(14, 165, 233, 0.25);
    color: #38bdf8;
    border: 1px solid rgba(14, 165, 233, 0.5);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}}

QLabel#WarningIcon {{
    background-color: rgba(0, 240, 255, 0.2);
    color: #facc15;
    border: 1px solid rgba(0, 240, 255, 0.4);
    border-radius: 14px;
    font-size: 16px;
    padding: 2px;
}}

QFrame#OriginalBox {{
    background-color: rgba(22, 28, 45, 0.7);
    border: 1px dashed rgba(148, 163, 184, 0.35);
    border-radius: 10px;
    padding: 6px;
}}

QFrame#ConvertedBox {{
    background-color: rgba(6, 78, 59, 0.35);
    border: 1px solid #10b981;
    border-radius: 10px;
    padding: 6px;
}}

QLabel#OriginalLabel {{
    color: #94a3b8;
    font-size: 12px;
}}

QLabel#OriginalValue {{
    color: #cbd5e1;
    font-size: 13px;
    font-family: Consolas, monospace;
}}

QLabel#ConvertedLabel {{
    color: #34d399;
    font-size: 12px;
    font-weight: 600;
}}

QLabel#ConvertedValue {{
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
}}

QPushButton#CopyButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34d399, stop:1 #059669);
    color: #064e3b;
    border: none;
    border-radius: 10px;
    padding: 9px 16px;
    font-weight: bold;
    font-size: 12px;
}}

QPushButton#CopyButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6ee7b7, stop:1 #10b981);
}}

QPushButton#ReplaceButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d2ff, stop:1 #0284c7);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 9px 16px;
    font-weight: bold;
    font-size: 12px;
}}

QPushButton#ReplaceButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #0ea5e9);
}}

QPushButton#CloseButton {{
    background-color: transparent;
    color: #94a3b8;
    border: none;
    font-size: 15px;
    font-weight: bold;
    border-radius: 6px;
}}

QPushButton#CloseButton:hover {{
    background-color: rgba(239, 68, 68, 0.25);
    color: #ef4444;
}}

QProgressBar#CountdownBar {{
    background-color: rgba(255, 255, 255, 0.08);
    border: none;
    border-radius: 2px;
    height: 4px;
}}

QProgressBar#CountdownBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00f0ff, stop:1 #10b981);
    border-radius: 2px;
}}
"""
