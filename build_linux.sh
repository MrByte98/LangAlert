#!/usr/bin/env bash
# Automated Standalone Builder for Linux (Ubuntu / Debian / Fedora / Arch)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "Building LangAlert Standalone Executable on Linux..."
echo "============================================================"

# Check Python3
command -v python3 >/dev/null 2>&1 || {
    echo "ERROR: python3 is required. Please install python3 (e.g., sudo apt install python3 python3-pip python3-venv)"
    exit 1
}

# Install / verify requirements and pyinstaller
echo ">> Checking and installing dependencies..."
python3 -m pip install --quiet --upgrade pip
python3 -m pip install --quiet -r requirements.txt
python3 -m pip install --quiet pyinstaller

# Run build script
echo ">> Packaging with PyInstaller..."
python3 build_standalone.py

# Package into tar.gz
echo ">> Creating tar.gz package..."
mkdir -p dist/packages
cd dist
tar -czvf packages/LangAlert-linux-x86_64.tar.gz LangAlert
cd ..

echo "============================================================"
echo "BUILD SUCCESSFUL! Linux standalone package:"
echo "dist/packages/LangAlert-linux-x86_64.tar.gz"
echo "============================================================"
