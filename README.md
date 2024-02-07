# SSRCL - Steam Stream Resolution Changer for Linux

Python script written with the help of ChatGPT.

**I made this for my own use. This is my first approach with python and i know nothing about it. Yes my code is bad and I know it. No pretention here.**

The goal of this project is to fix steam resolution not changing on linux when streaming with remote play.<br/>
Also muting host audio when streaming (this can be disabled)<br/>
This will only work with **X11** since i'm using xrandr for resolution changes.
Experimental support is present for Gnome wayland only.

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

- openrgb (toggle RGB to single color on stream)
- pactl (mute audio on host)
- gnome-randr-rust (gnome wayland support)

## How to install

Make sure you satisfy the required dependencies

Clone this repository and enter the directory

`https://gitlab.com/aethernali.live/ssrcl-steam-stream-resolution-changer-for-linux.git`

`cd ssrcl-steam-stream-resolution-changer-for-linux`

Run install.sh. You can add --autostart argument to create a desktop file in .config/autostart

`./install.sh` or `./install.sh --autostart`

To uninstall run

`/install.sh --uninstall`

## How to use

Run `steam_stream_resolution_changer` from a terminal.

Arguments:

- `-a, --audio` play audio on the host
- `-c, --client-resolution "WidthXHeight"` bypass client resolution autodetection.
Usefull if the resolution take too much time to set and if you always stream to the same device.
- `-o, --openrgb "HexColorCode"` Use OpenRGB to turn on your lights to the desired color when stream is active. Turn off at stream end.

## How does it work

This looks for some defined strings in `~/.steam/steam/logs/streaming_log.txt` to know if a stream is started or stopped.<br/>
It then set your monitor to the client resolution.
