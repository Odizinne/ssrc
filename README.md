# SSRC - Steam Stream Resolution Changer (for Linux)

The goal of this project is to fix desktop resolution not matching client resolution when streaming with remote play on linux host.<br/>
Also muting host audio when streaming (this can be disabled).<br/>
This will only work with **X11** since i'm using xrandr for resolution changes.

## Benefits

While you can stream at your native screen resolution, it may not be optimal:

- Incorrect scale (hard to read texts).
- Incorrect aspect ratio, leading to black bars.
- Wasted performances (i can run any game at 1280x800@90 at high / ultra settings, but cannot do it at 1440p).

## Requirements

- xrandr
- python3
- watchdog
- pyinstaller

Optional:

- openrgb (toggle RGB to single color when stream is on)
- pactl (mute audio on host)

## How to install

Make sure you satisfy the required dependencies.

Clone this repository and enter the directory:

`git clone https://github.com/Odizinne/ssrc.git`

`cd ssrc`

Run install.sh. You can add --autostart argument to create a user systemd service:

`./install.sh` or `./install.sh --autostart`

To uninstall run:

`/install.sh --uninstall`

## How to use

Run `ssrc` from a terminal.

Arguments:

- `-a, --audio` Play audio on the host.
- `-o, --openrgb "HexColorCode"` Use OpenRGB to turn on your lights to the desired color when stream is active. Turn off at stream end.

## How does it work

This looks for some defined strings in `~/.steam/steam/logs/streaming_log.txt` to know if a stream is started or stopped.<br/>
It then set your monitor to the client resolution.
