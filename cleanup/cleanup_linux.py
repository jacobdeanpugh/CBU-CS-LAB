import os
import shutil
import subprocess
from pathlib import Path

def clean_browser_cache():
    home = Path.home()

    subprocess.run(["pkill", "-u", os.getlogin(), "chrome"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-u", os.getlogin(), "firefox"], stderr=subprocess.DEVNULL)

    # Define paths to common browser cache directories
    targets = [
        home / ".cache/google-chrome/Default/Cache",
        home / ".cache/google-chrome/Default/Code Cache",
        home / ".cache/mozilla/firefox"
    ]

    for target in targets:
        if not target.exists():
            continue

        try:
            if "mozilla" in str(target):
                for cache_dir in target.glob("*/cache2"):
                    shutil.rmtree(cache_dir)
                    cache_dir.mkdir(parents=True, exist_ok=True)
            else:
                shutil.rmtree(target)
                target.mkdir(parents=True, exist_ok=True)

            print(f"Cleaned cache at: {target}")

        except Exception as e:
            print(f"Failed to clean {target}: {e}")

if __name__ == "__main__":
    clean_browser_cache()