
import os
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

#Database set-up
DB_FILE = "file_uploads.db"

def initialize_database():
    """Initialize the PLUSSQL database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

#Event Handler
class FileUploadHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_created(self, event):
        """Triggered when a new file is created."""
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            print(f"New file detected: {file_name}")

            #Log the file details to the database
            self.log_to_database(file_name, file_path)

    @staticmethod
    def log_to_database(filename, filepath):
        """Log the file details to the database."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO uploads (filename, filepath) VALUES (?, ?)", (filename, filepath))
        conn.commit()
        conn.close()
        print(f"Logged to database: {filename}")

#Main Function
def monitor_directory(directory):
    """Monitor a directory for file uploads."""
    event_handler = FileUploadHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"Monitoring directory: {directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    #install database
    initialize_database()

    #the directory to monitor
    directory_to_monitor = "./uploads"

    #the directory exists
    if not os.path.exists(directory_to_monitor):
        os.makedirs(directory_to_monitor)

    #Start monitoring the directory
    monitor_directory(directory_to_monitor)



