"""
Automated standalone builder for LangAlert (Windows, macOS, Linux).
Packages the application into an executable without requiring Python on the target machine.
"""
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"

def build():
    print("=" * 60)
    print(f"Building LangAlert Standalone Executable on {sys.platform}...")
    print("=" * 60)

    # Pre-render sounds
    from langswitch.sound_player import sound_player
    print("Ensuring sounds are pre-rendered...")
    sound_player._ensure_sound_files()

    # PyInstaller arguments
    separator = ";" if sys.platform == "win32" else ":"
    data_dict = f"langswitch/dictionaries{separator}langswitch/dictionaries"
    data_fonts = f"langswitch/fonts{separator}langswitch/fonts"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--name=LangAlert",
        "--clean",
        "--collect-all", "pynput",
        "--add-data", data_dict,
        "--add-data", data_fonts,
        "run.py"
    ]

    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        print(f"Executable generated in: {DIST_DIR / 'LangAlert'}")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        print("Note: Ensure pyinstaller is installed: pip install pyinstaller")

if __name__ == "__main__":
    build()
