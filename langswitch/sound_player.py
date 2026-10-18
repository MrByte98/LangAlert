"""
Cross-platform sound notification service for LangAlert.
Pre-renders clean harmonic chime waveforms to disk and provides
non-blocking asynchronous audio playback on Windows, macOS, and Linux.
"""
import math
import os
import struct
import subprocess
import sys
import threading
from pathlib import Path

from .config import config, get_app_data_dir

SOUNDS_DIR = get_app_data_dir() / "sounds"
SOUNDS_DIR.mkdir(parents=True, exist_ok=True)

TONE_SPECS = {
    "crystal_chime": {
        "freqs": [(880.0, 0.6), (1318.5, 0.4)],  # A5 + E6 chime
        "duration": 0.35,
        "decay": 6.5,
    },
    "subtle_bell": {
        "freqs": [(659.25, 0.7), (987.77, 0.3)], # E5 + B5 warm bell
        "duration": 0.40,
        "decay": 5.5,
    },
    "modern_beep": {
        "freqs": [(1046.5, 0.8), (1567.98, 0.2)], # C6 high ping
        "duration": 0.22,
        "decay": 8.0,
    }
}

class SoundPlayer:
    def __init__(self):
        self._sound_files = {}
        self._ensure_sound_files()

    def _ensure_sound_files(self):
        """Generates WAV files on disk if they don't already exist."""
        for name, spec in TONE_SPECS.items():
            fpath = SOUNDS_DIR / f"{name}.wav"
            if not fpath.exists():
                self._render_wav(fpath, spec)
            self._sound_files[name] = str(fpath)

    def _render_wav(self, filepath: Path, spec: dict):
        sample_rate = 44100
        duration = spec["duration"]
        num_samples = int(sample_rate * duration)
        freqs = spec["freqs"]
        decay_rate = spec["decay"]

        with open(filepath, "wb") as f:
            # WAV Header
            f.write(b"RIFF")
            f.write(struct.pack("<I", 36 + num_samples * 2))
            f.write(b"WAVEfmt ")
            f.write(struct.pack("<I", 16))            # Subchunk1Size
            f.write(struct.pack("<H", 1))             # AudioFormat (PCM)
            f.write(struct.pack("<H", 1))             # NumChannels (Mono)
            f.write(struct.pack("<I", sample_rate))   # SampleRate
            f.write(struct.pack("<I", sample_rate * 2))# ByteRate
            f.write(struct.pack("<H", 2))             # BlockAlign
            f.write(struct.pack("<H", 16))            # BitsPerSample
            f.write(b"data")
            f.write(struct.pack("<I", num_samples * 2))

            for i in range(num_samples):
                t = i / sample_rate
                # Smooth envelope: fast attack, exponential decay
                env = (1.0 - math.exp(-t * 200.0)) * math.exp(-decay_rate * (t / duration))

                sample_float = 0.0
                for freq, amp in freqs:
                    sample_float += amp * math.sin(2.0 * math.pi * freq * t)

                sample_val = int(max(-32767, min(32767, sample_float * env * 22000)))
                f.write(struct.pack("<h", sample_val))

    def play(self, tone_name: str = None):
        """Plays the specified or configured tone asynchronously."""
        if not config.get("sound_enabled", True):
            return

        tone = tone_name or config.get("sound_tone", "crystal_chime")
        filepath = self._sound_files.get(tone) or self._sound_files.get("crystal_chime")
        if not filepath or not os.path.exists(filepath):
            return

        if sys.platform == "win32":
            try:
                import winsound
                winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                print(f"[SoundPlayer] Windows audio error: {e}")
        elif sys.platform == "darwin":
            threading.Thread(target=self._play_mac, args=(filepath,), daemon=True).start()
        else:
            threading.Thread(target=self._play_linux, args=(filepath,), daemon=True).start()

    def _play_mac(self, filepath: str):
        try:
            subprocess.run(["afplay", filepath], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def _play_linux(self, filepath: str):
        # Try pulse audio or alsa
        for cmd in ["paplay", "aplay", "play"]:
            try:
                res = subprocess.run([cmd, filepath], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if res.returncode == 0:
                    break
            except Exception:
                continue

# Global sound player singleton
sound_player = SoundPlayer()
