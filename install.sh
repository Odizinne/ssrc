#!/bin/bash

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python before proceeding."
    exit 1
fi

echo "Copying ssrc and gnome-randr to /usr/local/bin."

sudo cp ssrc /usr/local/bin
sudo cp gnome-randr /usr/local/bin

mkdir -p ~/.config/systemd/user

cat <<EOF > ~/.config/systemd/user/ssrc.service
[Unit]
Description=Steam stream daemon
After=gnome-session-wayland@gnome.target

[Service]
Type=simple
ExecStart=/usr/local/bin/ssrc

[Install]
WantedBy=graphical-session.target
EOF

echo "Created ~/.config/systemd/user/ssrc.service."

systemctl --user enable ssrc.service
systemctl --user start ssrc.service

echo "Enabled and started ssrc.service."