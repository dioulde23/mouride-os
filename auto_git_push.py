import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoPushHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"[🌀] Changement détecté : {event.src_path}")
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "🔄 Commit automatique via IA"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("[✅] Changements poussés sur GitHub.")
        except subprocess.CalledProcessError:
            print("[⚠️] Aucun changement à commit.")

if __name__ == "__main__":
    path = "."  # Dossier actuel
    print(f"[👁️‍🗨️] Surveillance du dossier : {path}")
    event_handler = GitAutoPushHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
