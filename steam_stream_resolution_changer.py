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

def process_line(line):
    global default_adapter
    global default_resolution

    if "Maximum capture:" in line:
        match = re.search(r'\d+x\d+', line)
        if match:
            resolution = match.group()
            print(f"Applying stream resolution: {resolution}")
            os.system(f"xrandr --output {default_adapter} --mode {resolution}")

            if not args.audio:
                print("Muting host audio")
                os.system("pactl set-sink-mute @DEFAULT_SINK@ true")
    elif "terminated" in line and line not in initial_lines and line not in processed_lines:
        print("Applying default desktop resolution")
        processed_lines.add(line)
        os.system(f"xrandr --output {default_adapter} --mode {default_resolution}")

        if not args.audio:
            print("Resuming host audio")
            os.system("pactl set-sink-mute @DEFAULT_SINK@ false")

default_adapter, default_resolution = get_default_resolution_and_adapter()

print(f"Default Desktop Resolution: {default_resolution}")
print(f"Default Display Adapter: {default_adapter}")

if args.audio:
     print("Playing audio on host: enabled")
else:
     print("Playing audio on host: disabled")

file_path = os.path.expanduser("~/.steam/steam/logs/streaming_log.txt")

with open(file_path, 'r') as file:
    initial_lines = file.readlines()

processed_lines = set()

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
