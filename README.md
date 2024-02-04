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

## How to use

Get your adapter name and modes by running `xrandr`
Edit the file to set your adapter name, display resolution, and stream resolution.

If your display does not support your desired stream resolution, you might be able to create it. You can see plenty of tutorials online (xrandr create custom resolution)

`python3 steam_stream_resolution_change.py`

I recommend to autostart it.

## How does it work

This script looks for some defined strings in `~/.steam/steam/logs/streaming_log.txt` to know if a stream is started or stopped.

It uses xrandr to set the specified resolutions.

## What to improve

- Use variable to detect if running X/Wayland
- Implement something to change resolution on Wayland (as far as i know there is no "official" way to do it)
- Get python skills