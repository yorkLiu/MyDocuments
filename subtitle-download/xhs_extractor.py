#!/usr/bin/env python3
"""
Xiaohongshu (小红书) Note/Video Extractor
Wrapper for chubbyskills/xiaohongshu-ingest fetch_note.py

Output:
- Videos (if video note): /data/hermes/workspace/MyDocuments/subtitle-download/videos/
- Subtitles/Markdown: /data/hermes/workspace/MyDocuments/subtitle-download/subtitles/

Usage:
    python3 xhs_extractor.py "https://www.xiaohongshu.com/explore/xxx"
    python3 xhs_extractor.py "https://xhslink.com/xxx"
    export XHS_COOKIE="your_cookie"  # Recommended to avoid rate limiting
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

# Add skills directory to path
SKILLS_DIR = Path("/data/hermes/workspace/MyDocuments/subtitle-download/skills")
XHS_INGEST_DIR = SKILLS_DIR / "xiaohongshu-ingest"
FETCH_SCRIPT = XHS_INGEST_DIR / "scripts" / "fetch_note.py"

# Output directories
BASE_OUTPUT = Path("/data/hermes/workspace/MyDocuments/subtitle-download")
VIDEOS_DIR = BASE_OUTPUT / "videos"
SUBTITLES_DIR = BASE_OUTPUT / "subtitles"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 xhs_extractor.py <xhs_url> [--no-images] [--no-video] [--fallback-text FILE]", file=sys.stderr)
        sys.exit(1)
    
    # Ensure output directories exist
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Build command for fetch_note.py
    cmd = [
        sys.executable,
        str(FETCH_SCRIPT),
        sys.argv[1],
        "--output", str(SUBTITLES_DIR),
    ]
    
    # Pass through additional args
    for arg in sys.argv[2:]:
        cmd.append(arg)
    
    # Run the extraction
    env = os.environ.copy()
    print(f"[xhs_extractor] Extracting: {sys.argv[1]}", file=sys.stderr)
    result = subprocess.run(cmd, env=env, capture_output=False)
    
    if result.returncode != 0:
        sys.exit(result.returncode)
    
    # The script prints the output path to stdout
    # We can't easily capture it here since we didn't capture stdout
    # But the markdown is saved to SUBTITLES_DIR
    
    print(f"[xhs_extractor] Done. Markdown saved to: {SUBTITLES_DIR}", file=sys.stderr)

if __name__ == "__main__":
    main()