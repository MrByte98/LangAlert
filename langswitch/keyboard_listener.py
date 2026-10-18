"""
Global background keyboard listener for LangAlert.
Captures keystrokes asynchronously via pynput, buffers words and phrases,
resolves active OS layout characters via Win32 APIs, and triggers
intelligent language layout evaluation via PyQt signals.
"""
import time
import threading
from typing import Optional
import pyperclip
from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal

from .config import config
from .detector import detector, DetectionResult
from .layout_detector import translate_vk_to_char, get_active_keyboard_layout

class KeyboardListener(QObject):
    # Signals emitted to the Qt Main Thread
    mismatch_detected = pyqtSignal(object)  # Emits DetectionResult
    status_changed = pyqtSignal(bool)       # Emits True if active, False if paused

    def __init__(self):
        super().__init__()
        self._listener: Optional[keyboard.Listener] = None
        self._controller = keyboard.Controller()
        self._buffer = ""
        self._lock = threading.Lock()
        self._active = True
        self._pause_timer: Optional[threading.Timer] = None
        self._last_alerted_text = ""
        self._last_alert_time = 0.0

    @property
    def is_active(self) -> bool:
        return self._active

    def set_active(self, active: bool):
        self._active = active
        if not active:
            self.clear_buffer()
        self.status_changed.emit(self._active)

    def toggle_active(self) -> bool:
        self.set_active(not self._active)
        return self._active

    def start(self):
        """Starts the global background keyboard hook."""
        if self._listener is not None:
            return
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        """Stops the global background keyboard hook."""
        if self._pause_timer:
            self._pause_timer.cancel()
        if self._listener:
            try:
                self._listener.stop()
            except Exception:
                pass
            self._listener = None

    def clear_buffer(self):
        with self._lock:
            self._buffer = ""
        if self._pause_timer:
            self._pause_timer.cancel()

    def _on_press(self, key):
        if not self._active or not config.get("enabled", True):
            return

        char = None

        # 1. First, attempt to resolve true character using active foreground window layout
        vk = getattr(key, "vk", None)
        scan = getattr(key, "_scan", None)
        if vk is not None:
            char = translate_vk_to_char(vk, scan)

        # 2. Fallback to pynput char attribute
        if not char:
            try:
                if hasattr(key, "char") and key.char:
                    char = key.char
            except AttributeError:
                char = None

        if char:
            with self._lock:
                self._buffer += char
                if len(self._buffer) > 80:
                    self._buffer = self._buffer[-80:]
            self._schedule_pause_check()
            return

        # Special non-printable keys
        if key == keyboard.Key.space:
            with self._lock:
                self._buffer += " "
                if len(self._buffer) > 80:
                    self._buffer = self._buffer[-80:]
            if config.get("trigger_on_space", True):
                self._trigger_check(reason="space")
            else:
                self._schedule_pause_check()

        elif key == keyboard.Key.enter:
            if config.get("trigger_on_enter", True):
                self._trigger_check(reason="enter")
            self.clear_buffer()

        elif key == keyboard.Key.backspace:
            with self._lock:
                if self._buffer:
                    self._buffer = self._buffer[:-1]
            self._schedule_pause_check()

        elif key in (keyboard.Key.tab, keyboard.Key.esc):
            self.clear_buffer()

    def _on_release(self, key):
        pass

    def _schedule_pause_check(self):
        """Schedules a timeout check after typing has paused."""
        if not config.get("trigger_on_pause", True):
            return

        if self._pause_timer:
            self._pause_timer.cancel()

        timeout_sec = config.get("detection_timeout_ms", 1000) / 1000.0
        self._pause_timer = threading.Timer(timeout_sec, self._on_pause_timeout)
        self._pause_timer.daemon = True
        self._pause_timer.start()

    def _on_pause_timeout(self):
        self._trigger_check(reason="pause")

    def _trigger_check(self, reason: str = ""):
        with self._lock:
            text = self._buffer.strip()

        if not text:
            return

        # Get active foreground window layout
        active_layout = get_active_keyboard_layout()

        # Evaluate full buffer
        result = detector.evaluate(text, active_layout=active_layout)

        # If full text didn't trigger, evaluate the last word
        if not result and " " in text:
            last_word = text.split(" ")[-1].strip()
            if last_word:
                result = detector.evaluate(last_word, active_layout=active_layout)

        if result:
            now = time.time()
            # Anti-spam guard: avoid duplicate notifications within 2.5 seconds
            if result.original_text == self._last_alerted_text and (now - self._last_alert_time) < 2.5:
                return

            self._last_alerted_text = result.original_text
            self._last_alert_time = now

            # Emit signal to Qt GUI thread
            self.mismatch_detected.emit(result)

    def replace_text(self, original_text: str, replacement_text: str):
        """
        Simulates backspace keystrokes to erase original text,
        then pastes replacement text from clipboard.
        """
        def _execute_replacement():
            time.sleep(0.08)  # Short delay for target window focus
            
            try:
                old_clipboard = pyperclip.paste()
            except Exception:
                old_clipboard = ""

            try:
                pyperclip.copy(replacement_text)
                time.sleep(0.04)

                chars_to_delete = len(original_text)
                for _ in range(chars_to_delete):
                    self._controller.press(keyboard.Key.backspace)
                    self._controller.release(keyboard.Key.backspace)
                    time.sleep(0.005)

                time.sleep(0.04)
                cmd_key = keyboard.Key.cmd if config.get("platform") == "darwin" else keyboard.Key.ctrl
                with self._controller.pressed(cmd_key):
                    self._controller.press('v')
                    self._controller.release('v')

            finally:
                def _restore():
                    time.sleep(0.5)
                    try:
                        if old_clipboard:
                            pyperclip.copy(old_clipboard)
                    except Exception:
                        pass
                threading.Thread(target=_restore, daemon=True).start()

        threading.Thread(target=_execute_replacement, daemon=True).start()
