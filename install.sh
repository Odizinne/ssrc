#!/bin/bash

usage() {
    echo "Usage: $0 [--autostart] [--uninstall]"
    exit 1
}

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_LOCATION="/usr/local/bin"

if [ "$1" == "--uninstall" ]; then
    UNINSTALL=true
else
    UNINSTALL=false
fi

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller is not installed. Please install it manually using 'pip install pyinstaller'."
    exit 1
fi

if [ "$UNINSTALL" = true ]; then
    systemctl --user disable ssrc.service
    systemctl --user stop ssrc.service
    sudo rm -f $INSTALL_LOCATION/ssrc
    USER_SERVICE_DIR="$HOME/.config/systemd/user/"
    USER_SERVICE="$USER_SERVICE_DIR/ssrc.service"
    rm -f "$USER_SERVICE"
    systemctl --user daemon-reload
    echo "Uninstallation completed."
    exit 0
fi

echo "Building standalone executable..."
pyinstaller --onefile ssrc.py &>/dev/null
sudo mv dist/ssrc $INSTALL_LOCATION
echo "Executable installed in $INSTALL_LOCATION"
rm -rf build/ dist/ __pycache__/ ssrc.spec

if [ "$1" == "--autostart" ]; then
    AUTOSTART=true
else
    AUTOSTART=false
fi

if [ "$AUTOSTART" = true ]; then
    USER_SERVICE_DIR="$HOME/.config/systemd/user/"
    USER_SERVICE="$USER_SERVICE_DIR/ssrc.service"
    mkdir -p "$USER_SERVICE_DIR"
        cat <<EOF > "$USER_SERVICE"
[Unit]
Description=Workaround for stream remote play match client resolution not working
StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
ExecStart=/usr/local/bin/ssrc
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=graphical-session.target
EOF

    systemctl --user daemon-reload
    systemctl --user enable ssrc.service &>/dev/null
    systemctl --user start ssrc.service
    echo "Autostart service created and activated"
fi

echo "Installation completed."
exit 0
