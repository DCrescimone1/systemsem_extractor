"""
File handling utilities
"""

from pathlib import Path
from typing import List
import fnmatch

def find_files_by_pattern(directory: Path, pattern: str) -> List[Path]:
    """Find files matching a pattern in directory and subdirectories"""
    matches = []
    for file_path in directory.rglob("*"):
        if file_path.is_file() and fnmatch.fnmatch(file_path.name, pattern):
            matches.append(file_path)
    return matches

def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, create if needed"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes"""
    if file_path.exists():
        return file_path.stat().st_size / (1024 * 1024)
    return 0.0