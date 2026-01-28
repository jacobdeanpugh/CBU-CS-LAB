import os
import shutil
import subprocess
from pathlib import Path

def deep_clean_browsers():
    home = Path.home()
    user = os.getlogin()

    # Kill processes first - crucial because SQLite files are locked while open
    subprocess.run(["pkill", "-u", user, "chrome"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-u", user, "firefox"], stderr=subprocess.DEVNULL)

    # 1. CHROME TARGETS
    chrome_base = home / ".config/google-chrome/Default"
    chrome_targets = [
        chrome_base / "Cookies",
        chrome_base / "Cookies-journal",
        chrome_base / "Local Storage",
        chrome_base / "Session Storage",
        home / ".cache/google-chrome" # The actual cache
    ]

    # 2. FIREFOX TARGETS
    firefox_base = home / ".mozilla/firefox"
    # Note: Firefox keeps cookies in the profile root, not the .cache folder
    
    # Clean Chrome
    for path in chrome_targets:
        try:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                path.unlink(missing_ok=True)
        except Exception as e:
            print(f"Error cleaning Chrome path {path}: {e}")

    # Clean Firefox Profiles
    if firefox_base.exists():
        # Firefox profiles are folders like 'abc123xy.default-release'
        for profile in firefox_base.glob("*default*"):
            try:
                # cookies.sqlite is what keeps them logged in
                (profile / "cookies.sqlite").unlink(missing_ok=True)
                (profile / "cookies.sqlite-wal").unlink(missing_ok=True)
                # storage/default holds site-specific login data/tokens
                shutil.rmtree(profile / "storage", ignore_errors=True)
                print(f"Logged out of Firefox profile: {profile.name}")
            except Exception as e:
                print(f"Error cleaning Firefox profile {profile}: {e}")

if __name__ == "__main__":
    deep_clean_browsers()
    print("Cleanup complete. Users have been signed out.")