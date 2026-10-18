"""
Entry point for LangAlert.
Initializes High-DPI scaling, parses launch arguments, and launches the application.
"""
import sys
import os

# Ensure current directory is on python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langswitch.app import LangAlertApp

def main():
    minimized = "--minimized" in sys.argv
    app = LangAlertApp()
    sys.exit(app.start(show_settings_on_start=not minimized))

if __name__ == "__main__":
    main()
