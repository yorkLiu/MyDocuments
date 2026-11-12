#!/usr/bin/env python3
"""
Video Text Extractor for Chinese Platforms (Xiaohongshu, Douyin, Bilibili)

Saves:
- Videos to: workspace/MyDocuments/subtitle-download/videos/
- Subtitles as .md to: workspace/MyDocuments/subtitle-download/subtitles/

Usage:
    python3 video_text_extractor.py "https://www.xiaohongshu.com/explore/xxx"
    python3 video_text_extractor.py "https://v.douyin.com/xxx" --whisper-model small
    python3 video_text_extractor.py "https://www.bilibili.com/video/BV1xxx"
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# ─── Constants ──────────────────────────────────────────────────────────────
SUPPORTED_PLATFORMS = {
    'xiaohongshu': {
        'patterns': [
            r'xiaohongshu\.com/(?:explore|discovery/item)/([\da-f]+)',
            r'xhslink\.(?:com|cn)/[\w-]+',
        ],
        'yt_dlp_ie': 'XiaoHongShu',
    },
    'douyin': {
        'patterns': [
            r'douyin\.com/video/(\d+)',
            r'v\.douyin\.com/[\w-]+',
            r'iesdouyin\.com/share/video/(\d+)',
        ],
        'yt_dlp_ie': 'Douyin',
    },
    'bilibili': {
        'patterns': [
            r'bilibili\.com/video/([aAbB][vV][^/?#&]+)',
            r'bilibili\.com/video/av(\d+)',
            r'b23\.tv/[\w-]+',
            r'bili\.app/[\w-]+',
        ],
        'yt_dlp_ie': 'BiliBili',
    },
}

DEFAULT_WHISPER_MODEL = 'base'
MAX_VIDEO_DURATION = 3600

# Output directories
BASE_OUTPUT_DIR = Path("/data/hermes/workspace/MyDocuments/subtitle-download")
VIDEOS_DIR = BASE_OUTPUT_DIR / "videos"
SUBTITLES_DIR = BASE_OUTPUT_DIR / "subtitles"

# ─── Helpers ────────────────────────────────────────────────────────────────

def log(msg: str, quiet: bool = False):
    if not quiet:
        print(f"[video-text-extractor] {msg}", file=sys.stderr)

def run_cmd(cmd: List[str], check: bool = True, capture: bool = True, timeout: int = 300) -> subprocess.CompletedProcess:
    log(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=capture, text=True, check=check, timeout=timeout)

def detect_platform(url: str) -> Optional[str]:
    url_lower = url.lower()
    for platform, config in SUPPORTED_PLATFORMS.items():
        for pattern in config['patterns']:
            if re.search(pattern, url_lower):
                return platform
    return None

def resolve_short_url(url: str) -> str:
    try:
        import requests
        r = requests.head(url, allow_redirects=True, timeout=10)
        return r.url
    except Exception as e:
        log(f"Warning: Failed to resolve short URL: {e}")
        return url

def sanitize_filename(name: str, max_len: int = 150) -> str:
    """Sanitize string for use as filename."""
    # Remove/replace invalid chars
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    name = re.sub(r'[\r\n\t]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    # Limit length
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name or "untitled"

def get_output_filename(metadata: Dict[str, Any]) -> str:
    """Generate output filename from metadata (title or description)."""
    title = metadata.get('title', '').strip()
    if title:
        return sanitize_filename(title)
    
    # Fallback to description
    desc = metadata.get('description', '').strip()
    if desc:
        # Take first 100 chars of description
        return sanitize_filename(desc[:100])
    
    # Last resort: uploader + timestamp
    uploader = metadata.get('uploader', 'unknown')
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return sanitize_filename(f"{uploader}_{timestamp}")

def download_video(url: str, output_dir: Path, quiet: bool = False) -> Tuple[Path, Dict[str, Any], str]:
    """
    Download video using yt-dlp. Returns (video_path, metadata, safe_title).
    """
    # Get metadata first
    log(f"Fetching metadata for: {url}")
    meta_cmd = [
        'yt-dlp',
        '--dump-json',
        '--no-download',
        '--no-warnings',
        url
    ]
    meta_result = run_cmd(meta_cmd, check=False)
    if meta_result.returncode != 0:
        raise RuntimeError(f"Failed to fetch metadata: {meta_result.stderr}")

    metadata = json.loads(meta_result.stdout)
    safe_title = get_output_filename(metadata)
    duration = metadata.get('duration', 0)
    
    if duration and duration > MAX_VIDEO_DURATION:
        log(f"Warning: Video duration ({duration}s) exceeds limit ({MAX_VIDEO_DURATION}s)")

    # Download video with safe_title as filename
    output_template = str(output_dir / f"{safe_title}.%(ext)s")
    
    log(f"Downloading video: {safe_title}")
    dl_cmd = [
        'yt-dlp',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', output_template,
        '--no-warnings',
        url
    ]
    dl_result = run_cmd(dl_cmd, check=False)
    if dl_result.returncode != 0:
        raise RuntimeError(f"Download failed: {dl_result.stderr}")

    # Find downloaded file
    for ext in ['.mp4', '.mkv', '.webm', '.mov']:
        video_path = output_dir / f"{safe_title}{ext}"
        if video_path.exists():
            return video_path, metadata, safe_title

    # Fallback
    for f in output_dir.glob("*"):
        if f.suffix in ['.mp4', '.mkv', '.webm', '.mov'] and f.stat().st_size > 10000:
            return f, metadata, safe_title

    raise RuntimeError("Downloaded video file not found")

def download_subtitles(url: str, output_dir: Path, lang: str) -> Optional[Path]:
    """Download subtitles for a specific language."""
    cmd = [
        'yt-dlp',
        '--write-subs',
        '--sub-langs', lang,
        '--sub-format', 'vtt',
        '--skip-download',
        '-o', str(output_dir / f"subs_%(id)s.%(ext)s"),
        '--no-warnings',
        url
    ]
    result = run_cmd(cmd, check=False)
    if result.returncode == 0:
        for f in output_dir.glob("*.vtt"):
            return f
    return None

def parse_vtt(vtt_path: Path) -> List[Dict[str, Any]]:
    """Parse VTT subtitle file into segments."""
    segments = []
    try:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = re.split(r'\n\n+', content)
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 2:
                continue
            time_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})', lines[0])
            if time_match:
                start = time_to_seconds(time_match.group(1))
                end = time_to_seconds(time_match.group(2))
                text = ' '.join(lines[1:]).strip()
                text = re.sub(r'<[^>]+>', '', text)
                if text:
                    segments.append({'start': start, 'end': end, 'text': text})
    except Exception as e:
        log(f"Warning: Failed to parse VTT: {e}")
    return segments

def time_to_seconds(time_str: str) -> float:
    parts = time_str.split(':')
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])

def extract_audio(video_path: Path, output_wav: Path) -> Optional[Path]:
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        str(output_wav)
    ]
    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        log("Warning: Audio extraction failed")
        return None
    if not output_wav.exists() or output_wav.stat().st_size == 0:
        log("Warning: Extracted audio is empty")
        return None
    return output_wav

def transcribe_with_whisper(wav_path: Path, model_name: str) -> Tuple[List[Dict], str]:
    # Try Python import first
    try:
        import whisper
        log(f"Loading Whisper model '{model_name}'...")
        model = whisper.load_model(model_name)
        log("Transcribing...")
        result = model.transcribe(str(wav_path))
        
        segments = []
        for seg in result.get('segments', []):
            segments.append({
                'start': round(seg['start'], 3),
                'end': round(seg['end'], 3),
                'text': seg['text'].strip(),
            })
        full_text = result.get('text', '').strip()
        return segments, full_text
    except ImportError:
        log("Whisper Python package not available, trying CLI...")

    # Try CLI
    whisper_bin = shutil.which('whisper')
    if not whisper_bin:
        log("Error: Whisper not installed. Install with: pip install openai-whisper")
        return [], ""
    
    tmp_dir = tempfile.mkdtemp(prefix="whisper_")
    try:
        cmd = [
            whisper_bin,
            str(wav_path),
            '--model', model_name,
            '--output_format', 'json',
            '--output_dir', tmp_dir,
        ]
        log(f"Transcribing via CLI with model '{model_name}'...")
        result = run_cmd(cmd, check=False)
        
        if result.returncode != 0:
            log(f"Warning: whisper CLI failed: {result.stderr[:200]}")
            return [], ""
        
        json_files = [f for f in os.listdir(tmp_dir) if f.endswith('.json')]
        if not json_files:
            return [], ""
        
        with open(os.path.join(tmp_dir, json_files[0]), 'r') as f:
            data = json.load(f)
        
        segments = []
        for seg in data.get('segments', []):
            segments.append({
                'start': round(seg.get('start', 0.0), 3),
                'end': round(seg.get('end', 0.0), 3),
                'text': seg.get('text', '').strip(),
            })
        full_text = data.get('text', '').strip()
        return segments, full_text
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    seconds = max(0, int(seconds))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def write_subtitle_markdown(
    subtitle_path: Path,
    metadata: Dict[str, Any],
    segments: List[Dict[str, Any]],
    full_text: str,
    source: str,
    subtitle_lang: Optional[str],
    whisper_model: Optional[str],
    original_url: str,
    resolved_url: str,
) -> None:
    """Write subtitle content as markdown file with full text as main content."""
    title = metadata.get('title', '').strip()
    uploader = metadata.get('uploader', '').strip()
    duration = metadata.get('duration', 0)
    description = metadata.get('description', '').strip()
    tags = metadata.get('tags', [])
    view_count = metadata.get('view_count', 0)
    like_count = metadata.get('like_count', 0)
    
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        # Header
        f.write(f"# {title or 'Untitled'}\n\n")
        
        # Metadata section
        f.write("## 视频信息\n\n")
        f.write(f"- **平台**: {metadata.get('platform', 'unknown')}\n")
        f.write(f"- **原始链接**: {original_url}\n")
        f.write(f"- **解析链接**: {resolved_url}\n")
        if uploader:
            f.write(f"- **作者**: {uploader}\n")
        if duration:
            f.write(f"- **时长**: {duration:.0f}秒 ({format_timestamp(duration)})\n")
        if view_count:
            f.write(f"- **播放量**: {view_count:,}\n")
        if like_count:
            f.write(f"- **点赞数**: {like_count:,}\n")
        f.write(f"- **文本来源**: {source}\n")
        if subtitle_lang:
            f.write(f"- **字幕语言**: {subtitle_lang}\n")
        if whisper_model:
            f.write(f"- **Whisper模型**: {whisper_model}\n")
        f.write(f"- **提取时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")
        
        # Description
        if description:
            f.write("## 视频描述\n\n")
            f.write(f"{description}\n\n")
        
        # Tags
        if tags:
            f.write("## 标签\n\n")
            f.write(", ".join(f"`{tag}`" for tag in tags))
            f.write("\n\n")
        
        # Full text - MAIN CONTENT (complete text without timeline)
        f.write("## 完整文本\n\n")
        if full_text:
            f.write(f"{full_text}\n\n")
        else:
            f.write("*无可用文本*\n\n")
        
        # Optional: timestamped segments at the end for reference
        if segments:
            f.write("---\n\n")
            f.write("## 时间轴字幕（参考）\n\n")
            for seg in segments:
                start_ts = format_timestamp(seg['start'])
                end_ts = format_timestamp(seg['end'])
                f.write(f"### [{start_ts} - {end_ts}]\n\n")
                f.write(f"{seg['text']}\n\n")

def extract_video_text(
    url: str,
    whisper_model: str = DEFAULT_WHISPER_MODEL,
    quiet: bool = False,
) -> Dict[str, Any]:
    """
    Main pipeline: URL → download video → extract text → save to output dirs.
    """
    start_time = time.time()
    
    # Ensure output directories exist
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    SUBTITLES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Resolve short URLs
    original_url = url
    url = resolve_short_url(url)
    if url != original_url:
        log(f"Resolved short URL: {url}")
    
    # Detect platform
    platform = detect_platform(url)
    if not platform:
        raise ValueError(f"Unsupported platform or URL format: {url}")
    log(f"Detected platform: {platform}")
    
    # Create temp directory for processing
    with tempfile.TemporaryDirectory(prefix="video_extract_") as tmpdir:
        tmpdir_path = Path(tmpdir)
        log(f"Working directory: {tmpdir}")
        
        # Download video to temp first
        video_path, metadata, safe_title = download_video(url, tmpdir_path, quiet)
        log(f"Downloaded: {video_path.name} ({video_path.stat().st_size/1024/1024:.1f} MB)")
        
        # Move video to permanent videos directory
        final_video_path = VIDEOS_DIR / video_path.name
        # Handle duplicate names
        if final_video_path.exists():
            stem = final_video_path.stem
            suffix = final_video_path.suffix
            counter = 1
            while final_video_path.exists():
                final_video_path = VIDEOS_DIR / f"{stem}_{counter}{suffix}"
                counter += 1
        shutil.move(str(video_path), str(final_video_path))
        log(f"Video saved to: {final_video_path}")
        
        # Add platform to metadata
        metadata['platform'] = platform
        
        # Try to get subtitles first
        subtitle_segments = []
        subtitle_text = ""
        subtitle_lang = None
        
        subs = metadata.get('subtitles', {})
        auto_subs = metadata.get('automatic_captions', {})
        available_langs = list(set(subs.keys()) | set(auto_subs.keys()))
        
        # Prefer Chinese subtitles
        target_lang = None
        for lang in ['zh', 'zh-Hans', 'zh-CN', 'zh-TW', 'zh-Hant', 'en']:
            if lang in available_langs:
                target_lang = lang
                break
        
        if target_lang:
            log(f"Downloading subtitles ({target_lang})...")
            vtt_path = download_subtitles(url, tmpdir_path, target_lang)
            if vtt_path:
                subtitle_segments = parse_vtt(vtt_path)
                subtitle_text = ' '.join([s['text'] for s in subtitle_segments])
                subtitle_lang = target_lang
                log(f"  Got {len(subtitle_segments)} subtitle segments")
        
        # If no subtitles, or as supplement, transcribe audio
        whisper_segments = []
        whisper_text = ""
        
        probe_cmd = ['ffprobe', '-v', 'quiet', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', str(video_path)]
        probe_result = run_cmd(probe_cmd, check=False)
        has_audio = 'audio' in probe_result.stdout
        
        if has_audio:
            log("Extracting audio for transcription...")
            wav_path = tmpdir_path / "audio.wav"
            if extract_audio(video_path, wav_path):
                log("Transcribing with Whisper...")
                whisper_segments, whisper_text = transcribe_with_whisper(wav_path, whisper_model)
                log(f"  Got {len(whisper_segments)} transcription segments")
        else:
            log("Video has no audio track, skipping transcription")
        
        # Combine results
        combined_segments = []
        combined_text = ""
        
        if subtitle_segments:
            combined_segments = subtitle_segments
            combined_text = subtitle_text
            source = "subtitles"
            if whisper_segments:
                source += " + whisper"
        elif whisper_segments:
            combined_segments = whisper_segments
            combined_text = whisper_text
            source = "whisper"
        else:
            source = "none"
        
        # Write subtitle markdown
        subtitle_md_path = SUBTITLES_DIR / f"{safe_title}.md"
        # Handle duplicate names
        if subtitle_md_path.exists():
            stem = subtitle_md_path.stem
            counter = 1
            while subtitle_md_path.exists():
                subtitle_md_path = SUBTITLES_DIR / f"{stem}_{counter}.md"
                counter += 1
        
        write_subtitle_markdown(
            subtitle_path=subtitle_md_path,
            metadata=metadata,
            segments=combined_segments,
            full_text=combined_text,
            source=source,
            subtitle_lang=subtitle_lang,
            whisper_model=whisper_model if whisper_segments else None,
            original_url=original_url,
            resolved_url=url,
        )
        log(f"Subtitle saved to: {subtitle_md_path}")
        
        # Build result
        result = {
            'platform': platform,
            'original_url': original_url,
            'resolved_url': url,
            'title': metadata.get('title', ''),
            'duration': metadata.get('duration', 0),
            'uploader': metadata.get('uploader', ''),
            'uploader_id': metadata.get('uploader_id', ''),
            'view_count': metadata.get('view_count', 0),
            'like_count': metadata.get('like_count', 0),
            'description': metadata.get('description', ''),
            'tags': metadata.get('tags', []),
            'thumbnail': metadata.get('thumbnail', ''),
            'text_source': source,
            'subtitle_language': subtitle_lang,
            'subtitles_available': available_langs,
            'segment_count': len(combined_segments),
            'text_length': len(combined_text),
            'video_path': str(final_video_path),
            'subtitle_path': str(subtitle_md_path),
            'whisper_model': whisper_model if whisper_segments else None,
            'processing_time_seconds': round(time.time() - start_time, 2),
        }
        
        return result

# ─── CLI ────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='video-text-extractor',
        description='Extract text from videos on Xiaohongshu, Douyin, Bilibili',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Output directories:
  Videos:    {VIDEOS_DIR}
  Subtitles: {SUBTITLES_DIR} (as .md files)

Examples:
  %(prog)s "https://www.xiaohongshu.com/explore/65f123abc..."
  %(prog)s "https://v.douyin.com/xyz123" --whisper-model small
  %(prog)s "https://www.bilibili.com/video/BV1xxx"
  %(prog)s "URL" -q
        """,
    )
    parser.add_argument('url', help='Video URL (supports share/short links)')
    parser.add_argument('--whisper-model', default=DEFAULT_WHISPER_MODEL,
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help=f'Whisper model size (default: {DEFAULT_WHISPER_MODEL})')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress progress output')
    parser.add_argument('--base-dir', default=str(BASE_OUTPUT_DIR),
                        help=f'Base output directory (default: {BASE_OUTPUT_DIR})')
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    
    # Override base dir if provided
    global BASE_OUTPUT_DIR, VIDEOS_DIR, SUBTITLES_DIR
    if args.base_dir != str(BASE_OUTPUT_DIR):
        BASE_OUTPUT_DIR = Path(args.base_dir)
        VIDEOS_DIR = BASE_OUTPUT_DIR / "videos"
        SUBTITLES_DIR = BASE_OUTPUT_DIR / "subtitles"
    
    # Check dependencies
    for cmd in ('yt-dlp', 'ffmpeg', 'ffprobe'):
        if not shutil.which(cmd):
            print(f"Error: {cmd} not found. Please install it first.", file=sys.stderr)
            sys.exit(1)
    
    try:
        result = extract_video_text(
            url=args.url,
            whisper_model=args.whisper_model,
            quiet=args.quiet,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Print summary
    print(json.dumps({
        'title': result['title'],
        'video_path': result['video_path'],
        'subtitle_path': result['subtitle_path'],
        'text_source': result['text_source'],
        'text_length': result['text_length'],
        'segment_count': result['segment_count'],
        'processing_time_seconds': result['processing_time_seconds'],
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()