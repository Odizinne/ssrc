import os
import re
import argparse

file_path = os.path.expanduser("~/.steam/steam/logs/streaming_log.txt")
command = f"tail -F {file_path}"
resolution_pattern = re.compile(r'Maximum capture: (\d+x\d+)')

# Open the log first to clear content (We do not want old entries)

file = open(file_path,"w")
file.close()

def get_x11_default_resolution_and_adapter():
    xrandr_output = os.popen("xrandr").read()
    match = re.search(r'(?P<adapter>\w+-\d+) connected primary (?P<resolution>\d+x\d+)', xrandr_output)

    if match:
        return match.group("adapter"), match.group("resolution")
    else:
        raise ValueError("Unable to extract default resolution and adapter from xrandr output")

def get_wayland_default_resolution_and_adapter():
    gnome_randr_output = os.popen("gnome-randr").read()

    adapter_match = re.search(r'(?:associated physical monitors:\n\s+)([^\s]+)', gnome_randr_output)
    wayland_adapter_name = adapter_match.group(1) if adapter_match else None

    resolution_pattern = re.compile(r'\b(\d{3,4}x\d{3,4}@\d{1,3}\.\d{3})\b')

    resolutions = resolution_pattern.findall(gnome_randr_output)

    unique_width_height = set()
    unique_resolutions = set()

    filtered_resolutions = []
    for resolution in resolutions:
        width_height = resolution.split('@')[0]
        if width_height not in unique_width_height:
            unique_width_height.add(width_height)
            unique_resolutions.add(resolution)
            filtered_resolutions.append(resolution)

    wayland_default_resolution = filtered_resolutions[0] if filtered_resolutions else None

    return wayland_adapter_name, wayland_default_resolution, filtered_resolutions

def start_stream(streaming_resolution, session_type, default_adapter, filtered_resolutions, wayland_adapter_name, wayland_default_resolution, args):
    print("Stream started")
    print(f"Requested client resolution: {streaming_resolution}")

    if session_type == "x11":
        os.system(f"xrandr --output {default_adapter} --mode {streaming_resolution}")
        print(f"Setting host to {streaming_resolution}")
    elif session_type == "wayland" and (matching_resolution := next((res for res in filtered_resolutions if streaming_resolution in res), None)):
        desired_res = matching_resolution
        print(f"Matching resolution found: {desired_res}")
        os.system(f"gnome-randr modify --mode {desired_res} {wayland_adapter_name}")

    if not args.audio:
        print("Muting host audio")
        os.system("pactl set-sink-mute @DEFAULT_SINK@ true")

    if args.openrgb:
        os.system(f"openrgb --noautoconnect -c {args.openrgb} > /dev/null 2>&1")


def stop_stream(session_type, default_adapter, default_resolution, wayland_adapter_name, wayland_default_resolution, args):
    print("Stream stopped")

    if session_type == "x11":
        os.system(f"xrandr --output {default_adapter} --mode {default_resolution}")
        print(f"Setting host to {default_resolution}")
    elif session_type == "wayland":
        os.system(f"gnome-randr modify --mode {wayland_default_resolution} {wayland_adapter_name}")

    if not args.audio:
        print("Resuming host audio")
        os.system("pactl set-sink-mute @DEFAULT_SINK@ false")

    if args.openrgb:
        os.system("openrgb --noautoconnect -c 000000 > /dev/null 2>&1")

def main():
    parser = argparse.ArgumentParser(description="Monitor and adjust streaming settings.")
    parser.add_argument('-a', '--audio', action='store_true', help='Play audio on host')
    parser.add_argument('-c', '--client-resolution', help='Usage: -c "WidhtXHeight". Bypass client resolution detection by using a specified one')
    parser.add_argument('-o', '--openrgb', help='Usage: -o "hex color code". Apply the specified color to all LEDs supported by OpenRGB')

    args = parser.parse_args()
    print(f"User specified client res: {args.client_resolution}")
    print(f"RGB Color: {args.openrgb}")
    session_type = os.getenv('XDG_SESSION_TYPE')
    print(f"Session type: {session_type}")

    default_adapter, default_resolution, wayland_adapter_name, wayland_default_resolution, filtered_resolutions = None, None, None, None, None

    if session_type == "x11":
        default_adapter, default_resolution = get_x11_default_resolution_and_adapter()
        print(f"Default display Adapter: {default_adapter}")
        print(f"Default desktop Resolution: {default_resolution}")

    elif session_type == "wayland":
        wayland_adapter_name, wayland_default_resolution, filtered_resolutions = get_wayland_default_resolution_and_adapter()
        print("Wayland support is experimental and works only on Gnome with gnome-randr installed.")
        print(f"Default display Adapter: {wayland_adapter_name}")
        print(f"Default desktop resolution: {wayland_default_resolution}")

    if args.audio:
        print("Playing audio on host: enabled")
    else:
        print("Playing audio on host: disabled")

    with os.popen(command) as tail_output:
        for line in tail_output:
            if args.client_resolution and "Streaming initialized and listening" in line:
                streaming_resolution = args.client_resolution 
                start_stream(streaming_resolution, session_type, default_adapter, filtered_resolutions, wayland_adapter_name, wayland_default_resolution, args)

            if not args.client_resolution and "Maximum capture" in line:
                match = resolution_pattern.search(line)
                if match:
                    streaming_resolution = match.group(1)
                    start_stream(streaming_resolution, session_type, default_adapter, filtered_resolutions, wayland_adapter_name, wayland_default_resolution, args)

            if "connection terminated" in line:
                stop_stream(session_type, default_adapter, default_resolution, wayland_adapter_name, wayland_default_resolution, args)

if __name__ == "__main__":
    main()