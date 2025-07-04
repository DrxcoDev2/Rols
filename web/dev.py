# web/dev.py
import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_PATHS = ["../", "./templates", "./static", "./"]  

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, process_starter):
        self.restart = process_starter

    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.html', '.js', '.css')):
            print(f"[🔁] Archivo modificado: {event.src_path}")
            self.restart()

def start_server():
    print("[⚙️] Ejecutando: python web/setup.py")
    return subprocess.Popen(
        [sys.executable, "web/setup.py"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )




def main():
    print("[🚀] Iniciando servidor con autoreload...")
    process = start_server()

    def restart():
        nonlocal process
        if process:
            process.kill()
            process.wait()
        time.sleep(0.2)
        process = start_server()

    event_handler = ReloadHandler(restart)
    observer = Observer()

    for path in WATCH_PATHS:
        observer.schedule(event_handler, path=path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[⛔] Deteniendo servidor...")
        process.kill()
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
