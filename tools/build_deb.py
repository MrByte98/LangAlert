"""
Automated Debian/Ubuntu (.deb) Package Builder for LangAlert.
Can build native .deb packages on any operating system without requiring dpkg-deb.
"""
import os
import sys
import io
import time
import tarfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "dist"
PACKAGES_DIR = DIST_DIR / "packages"

VERSION = "1.0.1"
PACKAGE_NAME = "langalert"
ARCH = "amd64"
DEB_FILENAME = f"{PACKAGE_NAME}_{VERSION}_{ARCH}.deb"

def make_ar_header(name: str, size: int, mtime: int = None, mode: int = 0o100644) -> bytes:
    """Creates a 60-byte standard UNIX ar file header."""
    if mtime is None:
        mtime = int(time.time())
    header = f"{name:<16}{mtime:<12}{0:<6}{0:<6}{oct(mode)[2:]:<8}{size:<10}`\n"
    return header.encode("ascii")

def create_control_archive() -> bytes:
    """Generates control.tar.gz for Debian packaging."""
    control_content = f"""Package: {PACKAGE_NAME}
Version: {VERSION}
Section: utils
Priority: optional
Architecture: {ARCH}
Maintainer: MrByte98 <https://github.com/MrByte98/LangAlert>
Homepage: https://github.com/MrByte98/LangAlert
Depends: python3 (>= 3.10), python3-pip, libxkbcommon-x11-0, libxcb-cursor0
Description: Intelligent Keyboard Layout Mismatch Detection & Correction Utility
 LangAlert runs unobtrusively in the background system tray and instantly detects
 and corrects typing errors caused by wrong keyboard layout (Persian <-> English).
 Equipped with Character N-Gram statistical engine, Vazirmatn typography,
 and Cyber Neon Glassmorphism UI.
"""
    postinst_content = """#!/bin/sh
set -e
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q /usr/share/applications || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor || true
fi
exit 0
"""
    prerm_content = """#!/bin/sh
set -e
pkill -f "langalert" || true
exit 0
"""

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        # control file
        ti = tarfile.TarInfo("control")
        data = control_content.encode("utf-8")
        ti.size = len(data)
        ti.mode = 0o644
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(data))

        # postinst script
        ti = tarfile.TarInfo("postinst")
        data = postinst_content.encode("utf-8")
        ti.size = len(data)
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(data))

        # prerm script
        ti = tarfile.TarInfo("prerm")
        data = prerm_content.encode("utf-8")
        ti.size = len(data)
        ti.mode = 0o755
        ti.mtime = int(time.time())
        tar.addfile(ti, io.BytesIO(data))

    return buf.getvalue()

def create_data_archive() -> bytes:
    """Generates data.tar.gz containing /usr/bin, /usr/share and /opt/langalert."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        now = int(time.time())

        # 1. Desktop Entry: /usr/share/applications/langalert.desktop
        desktop_entry = """[Desktop Entry]
Name=LangAlert
Name[fa]=دستیار زبان کیبورد
Comment=Intelligent Keyboard Layout Mismatch Detection & Correction
Comment[fa]=تشخیص و اصلاح هوشمند چیدمان زبان کیبورد فارسی و انگلیسی
Exec=/usr/bin/langalert
Icon=langalert
Terminal=false
Type=Application
Categories=Utility;Accessibility;
StartupNotify=true
"""
        ti = tarfile.TarInfo("usr/share/applications/langalert.desktop")
        data = desktop_entry.encode("utf-8")
        ti.size = len(data)
        ti.mode = 0o644
        ti.mtime = now
        tar.addfile(ti, io.BytesIO(data))

        # 2. Icon: /usr/share/icons/hicolor/256x256/apps/langalert.png
        icon_path = BASE_DIR / "assets" / "icon.png"
        if icon_path.exists():
            with open(icon_path, "rb") as f:
                icon_data = f.read()
            ti = tarfile.TarInfo("usr/share/icons/hicolor/256x256/apps/langalert.png")
            ti.size = len(icon_data)
            ti.mode = 0o644
            ti.mtime = now
            tar.addfile(ti, io.BytesIO(icon_data))

        # 3. Executable wrapper: /usr/bin/langalert
        launcher_script = """#!/bin/sh
exec python3 /opt/langalert/run.py "$@"
"""
        ti = tarfile.TarInfo("usr/bin/langalert")
        data = launcher_script.encode("utf-8")
        ti.size = len(data)
        ti.mode = 0o755
        ti.mtime = now
        tar.addfile(ti, io.BytesIO(data))

        # 4. Application files: /opt/langalert/
        # Add run.py, requirements.txt, langswitch/ package, assets/
        files_to_pack = [
            ("run.py", BASE_DIR / "run.py"),
            ("requirements.txt", BASE_DIR / "requirements.txt"),
        ]
        for rel_name, abs_path in files_to_pack:
            if abs_path.exists():
                with open(abs_path, "rb") as f:
                    content = f.read()
                ti = tarfile.TarInfo(f"opt/langalert/{rel_name}")
                ti.size = len(content)
                ti.mode = 0o644
                ti.mtime = now
                tar.addfile(ti, io.BytesIO(content))

        # Walk langswitch directory
        langswitch_dir = BASE_DIR / "langswitch"
        for root, dirs, files in os.walk(langswitch_dir):
            if "__pycache__" in root:
                continue
            for file in files:
                if file.endswith((".pyc", ".pyo")):
                    continue
                fpath = Path(root) / file
                rel = fpath.relative_to(BASE_DIR).as_posix()
                with open(fpath, "rb") as f:
                    content = f.read()
                ti = tarfile.TarInfo(f"opt/langalert/{rel}")
                ti.size = len(content)
                ti.mode = 0o644
                ti.mtime = now
                tar.addfile(ti, io.BytesIO(content))

        # Assets
        assets_dir = BASE_DIR / "assets"
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                fpath = Path(root) / file
                rel = fpath.relative_to(BASE_DIR).as_posix()
                with open(fpath, "rb") as f:
                    content = f.read()
                ti = tarfile.TarInfo(f"opt/langalert/{rel}")
                ti.size = len(content)
                ti.mode = 0o644
                ti.mtime = now
                tar.addfile(ti, io.BytesIO(content))

    return buf.getvalue()

def build_deb():
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    deb_path = PACKAGES_DIR / DEB_FILENAME

    print(f"Building Debian package: {deb_path.name}...")

    debian_binary = b"2.0\n"
    control_tar_gz = create_control_archive()
    data_tar_gz = create_data_archive()

    with open(deb_path, "wb") as deb:
        # 1. Global AR magic
        deb.write(b"!<arch>\n")

        # 2. debian-binary member
        deb.write(make_ar_header("debian-binary", len(debian_binary)))
        deb.write(debian_binary)
        if len(debian_binary) % 2 != 0:
            deb.write(b"\n")

        # 3. control.tar.gz member
        deb.write(make_ar_header("control.tar.gz", len(control_tar_gz)))
        deb.write(control_tar_gz)
        if len(control_tar_gz) % 2 != 0:
            deb.write(b"\n")

        # 4. data.tar.gz member
        deb.write(make_ar_header("data.tar.gz", len(data_tar_gz)))
        deb.write(data_tar_gz)
        if len(data_tar_gz) % 2 != 0:
            deb.write(b"\n")

    size_kb = deb_path.stat().st_size / 1024
    print(f"SUCCESS! Package generated: {deb_path} ({size_kb:.1f} KB)")
    return deb_path

if __name__ == "__main__":
    build_deb()
