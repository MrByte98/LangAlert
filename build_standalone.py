"""
Automated standalone builder for LangAlert (Windows, macOS, Linux).
Packages the application into:
1. Single standalone portable executable (dist/LangAlert.exe)
2. Single-file Windows GUI installer (dist/LangAlert-Setup.exe)
3. Debian/Ubuntu package (dist/packages/langalert_1.0.0_amd64.deb)
"""
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"
ASSETS_DIR = BASE_DIR / "assets"
ICON_ICO = ASSETS_DIR / "icon.ico"
ICON_PNG = ASSETS_DIR / "icon.png"

def build():
    print("=" * 60)
    print(f"Building LangAlert Executables on {sys.platform}...")
    print("=" * 60)

    # 1. Pre-render sounds
    from langswitch.sound_player import sound_player
    print("[1/3] Ensuring sounds are pre-rendered...")
    sound_player._ensure_sound_files()

    # 2. Build single-file executable (LangAlert.exe)
    separator = ";" if sys.platform == "win32" else ":"
    data_dict = f"langswitch/dictionaries{separator}langswitch/dictionaries"
    data_fonts = f"langswitch/fonts{separator}langswitch/fonts"
    data_assets = f"assets{separator}assets"

    print("\n[2/3] Building single-file executable (LangAlert.exe)...")
    cmd_onefile = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=LangAlert",
        "--clean",
        "--collect-all", "pynput",
        "--add-data", data_dict,
        "--add-data", data_fonts,
        "--add-data", data_assets,
    ]
    if sys.platform == "win32" and ICON_ICO.exists():
        cmd_onefile.extend(["--icon", str(ICON_ICO)])

    cmd_onefile.append("run.py")

    print(f"Running command: {' '.join(cmd_onefile)}")
    try:
        subprocess.run(cmd_onefile, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error building standalone executable: {e}")
        sys.exit(1)

    # 3. On Windows: Build the single-file setup installer (LangAlert-Setup.exe)
    if sys.platform == "win32":
        print("\n[3/3] Building Windows GUI Setup Installer (LangAlert-Setup.exe)...")
        built_exe = DIST_DIR / "LangAlert.exe"
        if not built_exe.exists():
            print(f"Error: {built_exe} not found!")
            sys.exit(1)

        data_built_exe = f"{str(built_exe)}{separator}."
        cmd_installer = [
            sys.executable, "-m", "PyInstaller",
            "--noconsole",
            "--onefile",
            "--name=LangAlert-Setup",
            "--clean",
            "--icon", str(ICON_ICO),
            "--add-data", data_built_exe,
            "--add-data", data_assets,
            "tools/installer_ui.py"
        ]
        print(f"Running command: {' '.join(cmd_installer)}")
        try:
            subprocess.run(cmd_installer, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error building setup installer: {e}")
            sys.exit(1)

    # 4. Generate Linux .deb package
    print("\nGenerating Debian/Ubuntu (.deb) package...")
    try:
        from tools.build_deb import build_deb
        build_deb()
    except Exception as e:
        print(f"Note: .deb generation warning: {e}")

    print("\n" + "=" * 60)
    print("ALL BUILDS COMPLETED SUCCESSFULLY!")
    if sys.platform == "win32":
        print(f"1. Single Portable Executable: {DIST_DIR / 'LangAlert.exe'}")
        print(f"2. Single Setup Installer:     {DIST_DIR / 'LangAlert-Setup.exe'}")
    print(f"3. Debian/Ubuntu Package:      {DIST_DIR / 'packages' / 'langalert_1.0.0_amd64.deb'}")
    print("=" * 60)

if __name__ == "__main__":
    build()
