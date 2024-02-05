#!/bin/bash

usage() {
    echo "Usage: $0 [--autostart]"
    exit 1
}

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$1" == "--autostart" ]; then
    AUTOSTART=true
else
    AUTOSTART=false
fi

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller is not installed. Please install it manually using 'pip install pyinstaller'."
    exit 1
fi

cd "$SOURCE_DIR"

pyinstaller --onefile steam_stream_resolution_changer.py

sudo mv dist/steam_stream_resolution_changer /usr/local/bin/

rm -rf build/ dist/ __pycache__/ steam_stream_resolution_changer.spec

echo "Installation completed."

if [ "$AUTOSTART" = true ]; then
    AUTOSTART_DIR="$HOME/.config/autostart"
    DESKTOP_FILE="$AUTOSTART_DIR/steam_stream_resolution_changer.desktop"

    mkdir -p "$AUTOSTART_DIR"

    echo "[Desktop Entry]" > "$DESKTOP_FILE"
    echo "Type=Application" >> "$DESKTOP_FILE"
    echo "Name=Steam Stream Resolution Changer" >> "$DESKTOP_FILE"
    echo "Exec=/usr/local/bin/steam_stream_resolution_changer" >> "$DESKTOP_FILE"

    echo "Autostart file created: $DESKTOP_FILE"
fi

