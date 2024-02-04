import os
import sys
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_cursor_position(file):
    cursor_position = file.tell()
    return cursor_position

def parse_arguments():
    if len(sys.argv) < 2:
        print("You must specify desktop resolution, stream resolution, and adapter.")
        print("You can get information about the adapter and supported resolutions by running 'xrandr'.")
        print("Run this script with '--help' to get more information about arguments.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Monitor and change display settings based on log file events")
    parser.add_argument("-d", "--desktop-res", metavar='', help="Will apply when stream end.", required=True)
    parser.add_argument("-s", "--stream-res", metavar='', help="Will apply when stream start.", required=True)
    parser.add_argument("-a", "--adapter", metavar='', help="The screen you want to control.", required=True)
    args = parser.parse_args()

    args.desktop_res = args.desktop_res.strip('"')
    args.stream_res = args.stream_res.strip('"')

    return args

args = parse_arguments()

# Print the selected values
print(f"Selected Desktop Resolution: {args.desktop_res}")
print(f"Selected Streaming Resolution: {args.stream_res}")
print(f"Selected Display Adapter: {args.adapter}")

file_path = os.path.expanduser("~/.steam/steam/logs/streaming_log.txt")

# Create a list to store the initial lines in the file
initial_lines = []

# Open the file in read mode to read the initial lines
with open(file_path, 'r') as file:
    initial_lines = file.readlines()

# Create a set to store the processed lines
processed_lines = set()

# Initialize the variables for the cursor position, display, and resolutions
last_cursor_position = 0

class MyHandler(FileSystemEventHandler):
    def __init__(self, last_cursor_position):
        self.last_cursor_position = last_cursor_position

    def on_modified(self, event):
        if event.src_path == file_path:
            with open(file_path, 'r') as file:
                # Reposition the cursor to the last processed position
                file.seek(self.last_cursor_position)

                # Iterate through each line in the file
                for line in file:
                    # Check if the line contains "Streaming initialized" and is not in the initial lines or already processed
                    if "Streaming initialized" in line and line not in initial_lines and line not in processed_lines:
                        print("Applying stream resolution")
                        processed_lines.add(line)
                        os.system(f"xrandr --output {args.adapter} --mode {args.stream_res}")
                    # Check if the line contains "PulseAudio: Context connection terminated" and is not in the initial lines or already processed
                    elif "PulseAudio: Context connection terminated" in line and line not in initial_lines and line not in processed_lines:
                        print("Applying desktop resolution")
                        processed_lines.add(line)
                        os.system(f"xrandr --output {args.adapter} --mode {args.desktop_res}")

                # Update the last cursor position
                self.last_cursor_position = get_cursor_position(file)

observer = Observer()
event_handler = MyHandler(last_cursor_position)
observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
observer.start()

try:
    while True:
        time.sleep(.1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
