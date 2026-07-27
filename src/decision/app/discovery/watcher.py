from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.core.config import POLICIES_PATH
from app.discovery.policy_manager import PolicyManager
from app.discovery.sender import send_now


class PolicyWatcherHandler(FileSystemEventHandler):
    def handle_event(self, event):
        if event.is_directory or not str(event.src_path).endswith(".json"):
            return

        PolicyManager.reload_odrl()
        send_now()

    def on_modified(self, event):
        self.handle_event(event)

    def on_created(self, event):
        self.handle_event(event)

    def on_deleted(self, event):
        self.handle_event(event)


def start_policy_watcher():
    observer = Observer()
    observer.schedule(PolicyWatcherHandler(), POLICIES_PATH, recursive=False)
    observer.start()
    return observer
