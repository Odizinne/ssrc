# SSRCL - Steam Stream Resolution Changer for Linux

Stupid python script written 90% by ChatGPT. (i don't know python at all)

**I made this for my own use. This is my first approach with python and i know nothing about it. Yes my code is bad and I know it. No pretention here.**

The goal of this is to fix steam resolution not changing on linux when streaming with remote play.<br/>
This will only work with **X11** since i'm using xrandr for resolution changes.

It may not be optimal but it works.<br/>
Feel free to fork it, improve it, merge request it, or submit ideas.

## Benefits

While you can stream at your native screen resolution, it may not be optimal:

- Incorrect scale (hard to read texts).
- Incorrect aspect ratio, leading to black bars.
- Wasted performances (i can run any game at 1280x800@90 at high / ultra settings, but cannot do it at 1440p).

## Requirements

- xrandr
- python3
- watchdog (pip install watchdog)

The standalone executable should not require python3 or watchdog.

## How to use

[Download it](https://gitlab.com/aethernali.live/ssrcl-steam-stream-resolution-changer-for-linux/-/raw/main/steam_stream_resolution_changer?ref_type=heads&inline=false)


- `-a` Adapter name. 

Run `steam_stream_resolution_changer`.

You can add `-a` or `--audio` to play audio on host.
Default behavior is to mute host.

You can autostart it for a more seemless experience.

## How does it work

This script looks for some defined strings in `~/.steam/steam/logs/streaming_log.txt` to know if a stream is started or stopped.

It uses xrandr to set the specified resolutions.

## What to improve

Priority order

- **[DONE]** Adding automatic stream resolution based on client resolution
- **[DONE]** Adding automatic desktop resolution
- **[DONE]** Adding automatic adapter selection
- **[DONE]** Adding option to mute audio on host (since this is also broken in steam)
- Use variable to detect if running X/Wayland and print error message on wayland
- Implement something to change resolution on Wayland (as far as i know there is no "official" way to do it)
- Get python skills