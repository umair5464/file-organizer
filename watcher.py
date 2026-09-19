import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from organizer_core import organize_directory

def wait_until_file_ready(file_path: Path, timeout: float = 30.0) -> bool:
    """Ensures active browser downloads finish writing before moving."""
    # Instantly ignore temporary download files created by Chrome/Firefox
    if file_path.suffix in [".crdownload", ".part", ".tmp"]:
        return False

    start_time = time.time()
    last_size = -1

    while time.time() - start_time < timeout:
        if not file_path.exists():
            return False
        try:
            current_size = file_path.stat().st_size
            # If size is greater than 0 and hasn't changed over 0.5s, writing is complete
            if current_size == last_size and current_size > 0:
                return True
            last_size = current_size
        except (PermissionError, FileNotFoundError):
            pass
        time.sleep(0.5)
    return False

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, target_dir: str, category_states: dict = None):
        self.target_dir = Path(target_dir)
        self.category_states = category_states

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if wait_until_file_ready(file_path):
            print(f"Detected ready file: {file_path.name}")
            organize_directory(self.target_dir, self.category_states)

class FolderWatcher:
    def __init__(self, path_to_watch: str):
        self.path_to_watch = path_to_watch
        self.observer = None

    def start(self, category_states=None):
        self.observer = Observer()
        handler = DownloadHandler(self.path_to_watch, category_states)
        self.observer.schedule(handler, self.path_to_watch, recursive=False)
        self.observer.start()
        print(f"Monitoring started on: {self.path_to_watch}")

    def stop(self):
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            print("Monitoring stopped.")

if __name__ == "__main__":
    sandbox_path = str(Path("./test_downloads").resolve())
    watcher = FolderWatcher(sandbox_path)
    watcher.start()
    
    try:
        print("Live watcher active. Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()