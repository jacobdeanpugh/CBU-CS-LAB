import os
import shutil
import subprocess
from pathlib import Path

def sanatize_broswers():
    home = Path.home()
    
    # 1. Kill everything
    process_targets = [
        "chrome", "google-chrome", "google-chrome-stable", "chromium", 
        "brave", "msedge", "opera", "vivaldi", "chrome_crashpad"
    ]

    # 2. The Search Roots
    search_roots = [
        home / ".config",
        home / ".cache",      # Cache is huge
        home / ".local/share",
        home / ".var/app", 
        home / "snap"
    ]

    # 3. The "Nuclear" Target List
    target_names = {
        "Cookies", "cookies.sqlite", "Web Data", "History", "Login Data", 
        "Local Storage", "Session Storage", "IndexedDB", "storage",
        "Network", "Local State", "Preferences", "Sync Data", "GCM Store"
    }

    browser_keywords = ["chrome", "mozilla", "chromium", "brave", "opera", "microsoft-edge", "vivaldi"]

    print(f"🔍 Executing Nuclear Scrub...")
    
    for root_path in search_roots:
        if not root_path.exists(): continue
            
        for root, dirs, files in os.walk(root_path):
            current_path = Path(root)
            path_str = str(current_path).lower()
            
            # Ensure we are in a browser folder
            if not any(key in path_str for key in browser_keywords):
                continue

            current_items = set(dirs) | set(files)
            matches = target_names.intersection(current_items)

            for item in matches:
                target_path = current_path / item
                if target_path.exists():
                    try:
                        if target_path.is_dir():
                            shutil.rmtree(target_path, ignore_errors=True)
                        else:
                            target_path.unlink(missing_ok=True)
                        print(f"  [DESTROYED] -> {target_path}")
                    except:
                        pass

if __name__ == "__main__":
    sanatize_broswers() 
    print("\nBrowser cleanup complete.")