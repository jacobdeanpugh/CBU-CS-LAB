import os
import shutil
import subprocess
from pathlib import Path
import time

def force_logout_firefox():
    home = Path.home()
    user = os.getlogin()

    # 1. Kill EVERY possible Firefox process
    # We use -9 (SIGKILL) to ensure it doesn't try to "save session" on exit
    print("Forcefully closing all Firefox processes...")
    subprocess.run(["pkill", "-9", "-u", user, "firefox"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-9", "-u", user, "firefox-bin"], stderr=subprocess.DEVNULL)
    time.sleep(1) # Give the OS a second to release file locks

    # 2. Define the path to the Firefox config
    firefox_path = home / ".mozilla/firefox"

    if not firefox_path.exists():
        print("Firefox directory not found.")
        return

    # 3. Iterate through every profile folder
    # Profiles usually end in .default or .default-release
    for profile in firefox_path.glob("*"):
        if profile.is_dir():
            print(f"Cleaning profile: {profile.name}")
            
            # The "Nuclear" list of files that keep users logged in
            targets = [
                profile / "cookies.sqlite",
                profile / "cookies.sqlite-wal",
                profile / "cookies.sqlite-shm",
                profile / "sessionstore.jsonlz4", # THE main session file
                profile / "sessionstore-backups",   # Where Firefox hides recovery sessions
                profile / "storage",               # Where Gemini/Google store "IndexedDB" tokens
                profile / "webappsstore.sqlite",    # Local Storage
                profile / "indexedDB",             # Older location for site data
                profile / "permissions.sqlite"      # Site permissions/logins
            ]

            for target in targets:
                try:
                    if target.is_dir():
                        shutil.rmtree(target, ignore_errors=True)
                    else:
                        target.unlink(missing_ok=True)
                except Exception as e:
                    print(f"  [!] Could not delete {target.name}: {e}")

    # 4. Clear the Cache root as well
    cache_path = home / ".cache/mozilla/firefox"
    if cache_path.exists():
        shutil.rmtree(cache_path, ignore_errors=True)

if __name__ == "__main__":
    force_logout_firefox()
    print("\nDeep clean complete. Try opening Gemini now.")