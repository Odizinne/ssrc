import os
import re
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser(description="Monitor and adjust streaming settings.")
parser.add_argument('-a', '--audio', action='store_true', help='Play audio on host')
args = parser.parse_args()
def get_default_resolution_and_adapter():
    xrandr_output = os.popen("xrandr").read()
    match = re.search(r'(?P<adapter>\w+-\d+) connected primary (?P<resolution>\d+x\d+)', xrandr_output)

    if match:
        return match.group("adapter"), match.group("resolution")
    else:
        raise ValueError("Unable to extract default resolution and adapter from xrandr output")

stream_resolution = None
session_type = os.getenv('XDG_SESSION_TYPE')
file_path = os.path.expanduser("~/.steam/steam/logs/streaming_log.txt")

with open(file_path, 'r') as file:
    initial_lines = file.readlines()

processed_lines = set()

# This function parses gnome-randr output and extract adapter, default res, and every supported resolutions.

def wayland_get_available_resolutions():
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

#Display useful informations about your system.

print(f"Session type: {session_type}")

if session_type == "wayland":
    wayland_adapter_name, wayland_default_resolution, filtered_resolutions = wayland_get_available_resolutions()
    print("Wayland support is experimental and works only on Gnome with gnome-randr installed.")
    print(f"Default display Adapter: {wayland_adapter_name}")
    print(f"Default desktop resolution: {wayland_default_resolution}")

if session_type == "x11":
    default_adapter, default_resolution = get_default_resolution_and_adapter()
    print(f"Default display Adapter: {default_adapter}")
    print(f"Default desktop Resolution: {default_resolution}")

if args.audio:
     print("Playing audio on host: enabled")
else:
     print("Playing audio on host: disabled")

# Parse streaming_log.txt to know if streaming is started/stopped, and change resolution accordingly.
     
def process_line(line):
    if "Maximum capture:" in line:
        match = re.search(r'\d+x\d+', line)
        if match:
            stream_resolution = match.group()
            print(f"Client resolution: {stream_resolution}")
            if session_type == "x11":
                os.system(f"xrandr --output {default_adapter} --mode {stream_resolution}")
            if session_type == "wayland":
                matching_resolution = next((res for res in filtered_resolutions if stream_resolution in res), None)
                if matching_resolution:
                    desired_res = matching_resolution
                    print(f"Matching resolution found: {desired_res}")
                    os.system(f"gnome-randr modify --mode {desired_res} {wayland_adapter_name}")
            if not args.audio:
                print("Muting host audio")
                os.system("pactl set-sink-mute @DEFAULT_SINK@ true")
                
    elif "terminated" in line and line not in initial_lines and line not in processed_lines:
        print("Applying default desktop resolution")
        processed_lines.add(line)
        if session_type == "x11":
            os.system(f"xrandr --output {default_adapter} --mode {default_resolution}")

        if session_type == "wayland":
            os.system(f"gnome-randr modify --mode {wayland_default_resolution} {wayland_adapter_name}")

        if not args.audio:
            print("Resuming host audio")
            os.system("pactl set-sink-mute @DEFAULT_SINK@ false")

class StreamStatusMonitor(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_cursor_position = os.stat(self.file_path).st_size

    def on_modified(self, event):
        if event.src_path == self.file_path:
            with open(self.file_path, 'r') as file:
                file.seek(self.last_cursor_position)

                for line in file:
                    process_line(line)

                self.last_cursor_position = file.tell()

observer = Observer()
event_handler = StreamStatusMonitor(file_path)
observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
observer.start()

try:
    observer.join()
except KeyboardInterrupt:
    observer.stop()

observer.join()
