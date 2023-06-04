import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from app import message, util
from config import INPUT_DIR, TEMPLATE_DIR, STATIC_DIR
from site_generator import build_site


# Define the event handler that watches for changes to files
class BuildEventHandler(PatternMatchingEventHandler):

    def __init__(self):
        self.file_cache = {}
        super().__init__(patterns=['*.md', '*.html', '*.scss', '*.css', '*.js'], ignore_directories=True)

    def on_modified(self, event):
        """Whenever a file changes, cache the event and ignore further duplicate events. The cache does not
        currently remove any previous entries and continues to increase in size."""
        seconds = int(time.time())
        key = (seconds, event.src_path)
        if key in self.file_cache:
            return
        self.file_cache[key] = True
        util.clear_terminal()
        build_site()
        message.buffer_event.set()


def run():
    # Create an instance of the file-watching event handler
    event_handler = BuildEventHandler()

    # Create an observer to watch for changes to files
    observer = Observer()
    observer.schedule(event_handler, INPUT_DIR, recursive=True)
    observer.schedule(event_handler, TEMPLATE_DIR, recursive=True)
    observer.schedule(event_handler, STATIC_DIR, recursive=True)

    # Start the observer
    observer.start()
