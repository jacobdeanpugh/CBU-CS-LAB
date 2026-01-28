import os
import shutil
import subprocess
from pathlib import Path

def deep_clean_firefox():
    home = Path.home()
    user = os.getlogin()

    # 1. Kill Firefox - SQLite files are locked while the process is active
    print("Closing Firefox...")
    subprocess.run(["pkill", "-u", user, "firefox"], stderr=subprocess.DEVNULL)

    # 2. Define the Root Directories
    config_dir = home / ".mozilla/firefox"
    cache_root = home / ".cache/mozilla/firefox"

    # 3. Wipe the Cache (The heavy files)
    if cache_root.exists():
        try:
            shutil.rmtree(cache_root)
            print("Wiped all Firefox cache files.")
        except Exception as e:
            print(f"Error clearing cache: {e}")

    # 4. Wipe the Session Data (The login/account info)
    if config_dir.exists():
        # Firefox profiles are folders like 'x3j9l2.default-release'
        for profile in config_dir.glob("*default*"):
            # Files and folders to delete to ensure logout
            logout_targets = [
                profile / "cookies.sqlite",
                profile / "cookies.sqlite-wal",
                profile / "cookies.sqlite-shm",
                profile / "sessionstore-backups",
                profile / "storage", # This is where 'Local Storage' & tokens live
                profile / "formhistory.sqlite" # Optional: clears saved form data
            ]

            for target in logout_targets:
                try:
                    if target.is_dir():
                        shutil.rmtree(target, ignore_errors=True)
                    else:
                        target.unlink(missing_ok=True)
                except Exception as e:
                    print(f"Failed to delete {target.name}: {e}")
            
            print(f"User signed out of Firefox profile: {profile.name}")

if __name__ == "__main__":
    deep_clean_firefox()
    print("\nFirefox cleanup successful. All accounts signed out.")