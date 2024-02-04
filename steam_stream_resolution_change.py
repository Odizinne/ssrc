import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to get the current cursor position in the file
def get_cursor_position(file):
    cursor_position = file.tell()
    return cursor_position

# Specify the path to your file
file_path = os.path.expanduser("~/.steam/steam/logs/streaming_log.txt")

# Create a list to store the initial lines in the file
initial_lines = []

# Open the file in read mode to read the initial lines
with open(file_path, 'r') as file:
    initial_lines = file.readlines()

# Create a set to store the processed lines
processed_lines = set()

# Initialize the variable for the cursor position
last_cursor_position = 0

# Define a class to handle file modification events
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
                        print("started")
                        processed_lines.add(line)
                        os.system("xrandr --output DisplayPort-0 --mode 1280x800")
                    # Check if the line contains "PulseAudio: Context connection terminated" and is not in the initial lines or already processed
                    elif "PulseAudio: Context connection terminated" in line and line not in initial_lines and line not in processed_lines:
                        print("stopped")
                        processed_lines.add(line)
                        os.system("xrandr --output DisplayPort-0 --mode 2560x1440")

                # Update the last cursor position
                self.last_cursor_position = get_cursor_position(file)

# Instantiate an observer and attach the event handler
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
