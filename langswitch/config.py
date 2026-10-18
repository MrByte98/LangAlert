import json
import os
import sys
from pathlib import Path

def get_app_data_dir() -> Path:
    """Returns the platform-specific application data directory."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = Path(base) / "LangAlert"
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / "LangAlert"
    else:
        path = Path.home() / ".config" / "langalert"
    path.mkdir(parents=True, exist_ok=True)
    return path

CONFIG_FILE = get_app_data_dir() / "settings.json"

DEFAULT_CONFIG = {
    # Detection Settings
    "enabled": True,
    "check_en_to_fa": True,
    "check_fa_to_en": True,
    "min_word_length": 3,
    "detection_timeout_ms": 1000,
    "trigger_on_space": True,
    "trigger_on_enter": True,
    "trigger_on_pause": True,
    "sensitivity": "medium",  # "low", "medium", "high"
    
    # UI & Notification Settings
    "notification_position": "top_right",  # "top_right", "top_left", "bottom_right", "bottom_left"
    "notification_duration_sec": 6,        # Seconds before auto-dismiss
    "sound_enabled": True,
    "sound_tone": "crystal_chime",         # "crystal_chime", "subtle_bell", "modern_beep"
    "theme": "dark",                       # "dark", "light", "glassmorphism"
    "notification_opacity": 0.95,
    "window_opacity": 0.97,
    "auto_copy_on_click": True,
    "show_replace_button": True,
    "margin_x": 25,
    "margin_y": 45,
    
    # App Settings
    "start_minimized": True,
    "start_with_system": False,
    "history_max_items": 50,
}

class ConfigManager:
    """Manages application settings with automatic persistence to disk."""
    
    def __init__(self, filepath: Path = CONFIG_FILE):
        self.filepath = filepath
        self._data = dict(DEFAULT_CONFIG)
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self._data.update(saved)
            except Exception as e:
                print(f"[Config] Error loading config: {e}. Using defaults.")

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Config] Error saving config: {e}")

    def get(self, key: str, default=None):
        return self._data.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def set(self, key: str, value):
        self._data[key] = value
        self.save()

    def reset_to_defaults(self):
        self._data = dict(DEFAULT_CONFIG)
        self.save()

    def all(self) -> dict:
        return dict(self._data)

# Global singleton
config = ConfigManager()
