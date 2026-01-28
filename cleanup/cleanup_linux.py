import os
import shutil
import subprocess
from pathlib import Path

def deep_clean_snap_firefox():
    # The confirmed Snap path for Ubuntu
    home = Path.home()
    firefox_path = home / "snap/firefox/common/.mozilla/firefox"
    
    print(f"Targeting Snap directory: {firefox_path}")

    # 1. Kill Firefox processes (Forcefully)
    # This prevents Firefox from writing the session back to disk on exit
    subprocess.run(["pkill", "-9", "firefox"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-9", "firefox-bin"], stderr=subprocess.DEVNULL)

    if not firefox_path.exists():
        print("Error: Could not find the Firefox Snap directory.")
        return

    # 2. Iterate through profiles
    for profile in firefox_path.glob("*"):
        # We look for folders containing prefs.js to confirm it's a real profile
        if profile.is_dir() and (profile / "prefs.js").exists():
            print(f"Cleaning Profile: {profile.name}")
            
            # These are the specific targets for a full logout
            targets = [
                profile / "storage",               # Wipes Gemini/Google tokens
                profile / "cookies.sqlite",        # Wipes standard session cookies
                profile / "sessionstore.jsonlz4",  # Prevents tab restoration
                profile / "sessionstore-backups",  # Prevents recovery restoration
                profile / "indexedDB"              # Wipes modern web database data
            ]

            for target in targets:
                try:
                    if target.is_dir():
                        shutil.rmtree(target, ignore_errors=True)
                    else:
                        target.unlink(missing_ok=True)
                except Exception as e:
                    print(f"  [!] Failed to delete {target.name}: {e}")

    # 3. Clear the Snap-specific cache folder
    # Snaps often store heavy cache files here
    snap_cache = home / "snap/firefox/common/.cache/mozilla/firefox"
    if snap_cache.exists():
        shutil.rmtree(snap_cache, ignore_errors=True)
        print("Snap cache cleared.")

if __name__ == "__main__":
    deep_clean_snap_firefox()
    print("\nLogout complete. You should be cleared from Gemini.")