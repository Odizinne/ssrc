# SSRC - Steam Stream Resolution Changer (for Linux)

The goal of this project is to fix desktop resolution not matching client resolution when streaming with remote play on linux host.<br/>
Also muting host audio when streaming.<br/>
This will only work in gnome wayland.
Feel free to edit it to work with your DE.

## Benefits

While you can stream at your native screen resolution, it may not be optimal:

- Incorrect scale (hard to read texts).
- Incorrect aspect ratio, leading to black bars.
- Wasted performances (i can run any game at 1280x800@90 at high / ultra settings, but cannot do it at 1440p).

## Requirements

- python3
- pactl

## How to install

Make sure you satisfy the required dependencies.

Clone this repository and enter the directory:

`git clone https://github.com/Odizinne/ssrc.git`

`cd ssrc`

Run install.sh. You can add --autostart argument to create a user systemd service:

`./install.sh`

## How does it work

This looks for some defined strings in `~/.steam/steam/logs/streaming_log.txt` to know if a stream is started or stopped.<br/>
It then set your monitor to the client resolution with gnome-randr, and reset when stream is ending.


## Notes

I removed X11 support since this is deprecated.
You can still use ssrc.py if needed (won't be updated anymore)

I'll port some options from old X11ssrc to the new one when i have time / motivation.