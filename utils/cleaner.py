# utils/cleaner.py
import os
import time

def clean_old_files(folder, max_age_minutes=30):
    now = time.time()
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age_minutes * 60:
                try:
                    os.remove(file_path)
                    print(f"[CLEANER] Removed old file: {filename}")
                except Exception as e:
                    print(f"[CLEANER] Failed to delete {filename}: {e}")
