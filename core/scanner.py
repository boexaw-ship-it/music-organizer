import os
from pathlib import Path
from config import SUPPORTED_EXTENSIONS

try:
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.wave import WAVE
    from mutagen.mp4 import MP4
    from mutagen.id3 import ID3, ID3NoHeaderError
    from mutagen.easyid3 import EasyID3
    MUTAGEN_OK = True
except ImportError:
    MUTAGEN_OK = False


def _read_mp3(path: str) -> dict:
    info = {"artist": "", "album": "", "title": "", "has_artwork": False}
    try:
        tags = EasyID3(path)
        info["artist"] = tags.get("artist", [""])[0]
        info["album"]  = tags.get("album",  [""])[0]
        info["title"]  = tags.get("title",  [""])[0]
    except Exception:
        pass
    try:
        raw = ID3(path)
        info["has_artwork"] = any(k.startswith("APIC") for k in raw.keys())
    except Exception:
        pass
    return info


def _read_flac(path: str) -> dict:
    info = {"artist": "", "album": "", "title": "", "has_artwork": False}
    try:
        tags = FLAC(path)
        info["artist"] = (tags.get("artist") or [""])[0]
        info["album"]  = (tags.get("album")  or [""])[0]
        info["title"]  = (tags.get("title")  or [""])[0]
        info["has_artwork"] = bool(tags.pictures)
    except Exception:
        pass
    return info


def _read_wav(path: str) -> dict:
    info = {"artist": "", "album": "", "title": "", "has_artwork": False}
    try:
        tags = WAVE(path)
        easy = tags.tags
        if easy:
            info["artist"] = str(easy.get("TPE1", [""])[0]) if "TPE1" in easy else ""
            info["album"]  = str(easy.get("TALB", [""])[0]) if "TALB" in easy else ""
            info["title"]  = str(easy.get("TIT2", [""])[0]) if "TIT2" in easy else ""
    except Exception:
        pass
    return info


def _read_m4a(path: str) -> dict:
    info = {"artist": "", "album": "", "title": "", "has_artwork": False}
    try:
        tags = MP4(path)
        info["artist"] = (tags.get("\xa9ART") or [""])[0]
        info["album"]  = (tags.get("\xa9alb") or [""])[0]
        info["title"]  = (tags.get("\xa9nam") or [""])[0]
        info["has_artwork"] = bool(tags.get("covr"))
    except Exception:
        pass
    return info


_READERS = {
    ".mp3":  _read_mp3,
    ".flac": _read_flac,
    ".wav":  _read_wav,
    ".m4a":  _read_m4a,
}


def read_tags(path: str) -> dict:
    if not MUTAGEN_OK:
        return {"artist": "", "album": "", "title": "", "has_artwork": False}
    ext = Path(path).suffix.lower()
    reader = _READERS.get(ext)
    if reader:
        return reader(path)
    return {"artist": "", "album": "", "title": "", "has_artwork": False}


def scan_folder(folder: str) -> list[dict]:
    results = []
    for root, _, files in os.walk(folder):
        for fname in sorted(files):
            ext = Path(fname).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            full_path = os.path.join(root, fname)
            tags = read_tags(full_path)
            results.append({
                "path":        full_path,
                "filename":    fname,
                "ext":         ext,
                "artist":      tags["artist"] or "Unknown Artist",
                "album":       tags["album"]  or "Unknown Album",
                "title":       tags["title"]  or Path(fname).stem,
                "has_artwork": tags["has_artwork"],
                "mb_fetched":  False,
            })
    return results
