import os
import re
import argparse

file_path = os.path.expanduser("~/.steam/steam/logs/streaming_log.txt")
command = f"tail -F {file_path}"
resolution_pattern = re.compile(r'Maximum capture: (\d+x\d+)')

file = open(file_path,"w")
file.close()

def get_output_info():
    xrandr_output = os.popen("xrandr").read()
    match = re.search(r'(?P<adapter>\w+-\d+) connected primary (?P<resolution>\d+x\d+)', xrandr_output)

    if match:
        return match.group("adapter"), match.group("resolution")
    else:
        raise ValueError("Unable to extract default resolution and adapter from xrandr output")

def start_stream(default_adapter, streaming_resolution, args):
    print("Stream started")
    print(f"Requested client resolution: {streaming_resolution}")

    os.system(f"xrandr --output {default_adapter} --mode {streaming_resolution}")
    print(f"Setting host to {streaming_resolution}")

    if not args.audio:
        print("Muting host audio")
        os.system("pactl set-sink-mute @DEFAULT_SINK@ true")

    if args.openrgb:
        os.system(f"openrgb --noautoconnect -c {args.openrgb} > /dev/null 2>&1")

def stop_stream(default_adapter, default_resolution, args):
    print("Stream stopped")

    os.system(f"xrandr --output {default_adapter} --mode {default_resolution}")
    print(f"Setting host to {default_resolution}")

    if not args.audio:
        print("Resuming host audio")
        os.system("pactl set-sink-mute @DEFAULT_SINK@ false")

    if args.openrgb:
        os.system("openrgb --noautoconnect -c 000000 > /dev/null 2>&1")

def main():
    parser = argparse.ArgumentParser(description="Optional args.")
    parser.add_argument('-a', '--audio', action='store_true', help='Play audio on host')
    parser.add_argument('-o', '--openrgb', help='Usage: -o "hex color code". Apply the specified color to all LEDs supported by OpenRGB')

    args = parser.parse_args()
    session_type = os.getenv('XDG_SESSION_TYPE')

    if session_type == "x11":
        default_adapter, default_resolution = get_output_info()
        print(f"Default display Adapter: {default_adapter}")
        print(f"Default desktop Resolution: {default_resolution}")
    if session_type == "wayland":
        print("Wayland is not supported")
    if args.audio:
        print("Playing audio on host: enabled")
    if args.openrgb:
        print(f"RGB Color: {args.openrgb}")

    with os.popen(command) as tail_output:
        for line in tail_output:
            if "Maximum capture" in line and session_type == "x11":
                match = resolution_pattern.search(line)
                if match:
                    streaming_resolution = match.group(1)
                    start_stream(default_adapter, streaming_resolution, args)
            if "connection terminated" in line and session_type == "x11":
                stop_stream(default_adapter, default_resolution, args)

if __name__ == "__main__":
    main()

