"""
Active keyboard layout detector and keystroke character translator.
Determines whether the user's active foreground window is in Persian or English,
and resolves virtual key codes into the exact Unicode character for that layout.
"""
import sys
import ctypes
from typing import Optional, Tuple

if sys.platform == "win32":
    from ctypes import wintypes
    # Use private WinDLL instance so we do not mutate the process-wide ctypes.windll.user32
    user32 = ctypes.WinDLL("user32", use_last_error=True)

    user32.GetForegroundWindow.restype = wintypes.HWND
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetKeyboardLayout.argtypes = [wintypes.DWORD]
    user32.GetKeyboardLayout.restype = wintypes.HKL
    user32.GetKeyState.argtypes = [wintypes.INT]
    user32.GetKeyState.restype = wintypes.SHORT
    user32.MapVirtualKeyExW.argtypes = [wintypes.UINT, wintypes.UINT, wintypes.HKL]
    user32.MapVirtualKeyExW.restype = wintypes.UINT
    user32.ToUnicodeEx.argtypes = [
        wintypes.UINT, wintypes.UINT, ctypes.c_voidp,
        wintypes.LPWSTR, wintypes.INT, wintypes.UINT, wintypes.HKL
    ]
    user32.ToUnicodeEx.restype = wintypes.INT

def get_foreground_hkl():
    """Returns the HKL of the active foreground window, or default layout."""
    if sys.platform != "win32":
        return None
    hwnd = user32.GetForegroundWindow()
    if hwnd:
        tid = user32.GetWindowThreadProcessId(hwnd, None)
        hkl = user32.GetKeyboardLayout(tid)
        if hkl:
            return hkl
    return user32.GetKeyboardLayout(0)

def get_active_keyboard_layout() -> str:
    """
    Returns 'fa' if active foreground window is Persian,
    'en' if English, or 'unknown'.
    """
    if sys.platform == "win32":
        try:
            hkl = get_foreground_hkl()
            lang_id = (hkl or 0) & 0xFFFF
            if lang_id == 0x0429:
                return "fa"
            elif (lang_id & 0xFF) == 0x09:  # 0x0409 US, 0x0809 UK, etc.
                return "en"
            return "other"
        except Exception:
            return "unknown"
    elif sys.platform == "darwin":
        try:
            import subprocess
            out = subprocess.check_output(
                ["defaults", "read", "~/Library/Preferences/com.apple.HIToolbox.plist", "AppleSelectedInputSources"],
                timeout=0.2
            ).decode()
            if "Persian" in out or "Farsi" in out:
                return "fa"
            elif "US" in out or "ABC" in out:
                return "en"
        except Exception:
            pass
        return "unknown"
    else:
        try:
            import subprocess
            out = subprocess.check_output(["setxkbmap", "-query"], timeout=0.2).decode()
            for line in out.splitlines():
                if line.startswith("layout:"):
                    val = line.split(":", 1)[1].strip()
                    if "ir" in val or "fa" in val:
                        return "fa"
                    elif "us" in val or "en" in val:
                        return "en"
        except Exception:
            pass
        return "unknown"

def translate_vk_to_char(vk: int, scan: Optional[int] = None) -> Optional[str]:
    """
    Translates a virtual key code into the actual character produced
    in the active foreground window according to its current HKL and modifier keys.
    """
    if sys.platform != "win32" or vk is None:
        return None

    try:
        hkl = get_foreground_hkl()
        if not hkl:
            return None

        if scan is None or scan == 0:
            scan = user32.MapVirtualKeyExW(vk, 0, hkl)

        # Build modifier key state table
        kstate = (wintypes.BYTE * 256)()

        # Shift key (VK_SHIFT = 0x10)
        if user32.GetKeyState(0x10) & 0x8000:
            kstate[0x10] = 0x80
        # CapsLock key (VK_CAPITAL = 0x14)
        if user32.GetKeyState(0x14) & 1:
            kstate[0x14] = 1
        # Ctrl + Alt (AltGr)
        if user32.GetKeyState(0x11) & 0x8000:
            kstate[0x11] = 0x80
        if user32.GetKeyState(0x12) & 0x8000:
            kstate[0x12] = 0x80

        buff = ctypes.create_unicode_buffer(10)
        res = user32.ToUnicodeEx(vk, scan, kstate, buff, 10, 0, hkl)
        if res > 0:
            val = buff.value
            return val if len(val) == 1 else val[:1]
        return None
    except Exception:
        return None
