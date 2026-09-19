import os
import shutil
from pathlib import Path

# Category mapping
EXTENSION_MAP = {
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".svg"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "Documents": [".pdf", ".docx", ".xlsx", ".txt", ".csv", ".vcf", ".mwb"],
    "Archives": [".zip", ".tar.gz", ".tar", ".gz", ".7z", ".rar"],
    "Executables_and_Apps": [".appimage", ".exe", ".deb", ".rpm", ".gguf"]
}

def get_unique_path(dest_dir: Path, filename: str) -> Path:
    """Appends a counter (e.g., invoice(1).pdf) if a collision occurs."""
    target_path = dest_dir / filename
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1

    while True:
        new_path = dest_dir / f"{stem}({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

def organize_directory(source_dir: str, active_categories: dict = None):
    """Scans directory, filters out folders, and safely moves files."""
    source = Path(source_dir).resolve()
    if not source.exists():
        print(f"Error: Directory {source_dir} does not exist.")
        return

    for item in source.iterdir():
        # Critical Check: Strictly ignore directories to remain non-destructive
        if item.is_dir():
            continue

        file_ext = item.suffix.lower()
        
        for category, extensions in EXTENSION_MAP.items():
            # Check if this category is enabled (used later by GUI toggles)
            if active_categories and not active_categories.get(category, True):
                continue

            if file_ext in extensions:
                dest_category_dir = source / category
                dest_category_dir.mkdir(exist_ok=True)
                
                target_file_path = get_unique_path(dest_category_dir, item.name)
                shutil.move(str(item), str(target_file_path))
                print(f"Moved: {item.name} -> {target_file_path.relative_to(source)}")
                break

if __name__ == "__main__":
    # Test directly on our sandbox directory
    sandbox_dir = Path("./test_downloads")
    print("Testing core sorting logic on sandbox...\n")
    organize_directory(sandbox_dir)