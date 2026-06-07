import os
import re
import shutil
from pathlib import Path
from core.musicbrainz import get_release_mbid
from core.artwork import fetch_cover_art


def sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip() or "Unknown"


def build_dest_path(output_root: str, artist: str, album: str, title: str, ext: str) -> str:
    return os.path.join(
        output_root,
        sanitize(artist),
        sanitize(album),
        sanitize(title) + ext,
    )


def _unique_path(dest: str) -> str:
    if not os.path.exists(dest):
        return dest
    base, ext = os.path.splitext(dest)
    counter = 1
    while True:
        candidate = f"{base}_{counter}{ext}"
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def organize_files(files: list[dict], output_root: str, fetch_artwork: bool = True) -> dict:
    moved = []
    errors = []
    artwork_done: set[str] = set()

    for f in files:
        src    = f.get("path", "")
        artist = f.get("artist", "Unknown Artist")
        album  = f.get("album",  "Unknown Album")
        title  = f.get("title",  "track")
        ext    = f.get("ext",    Path(f.get("filename", "track.mp3")).suffix.lower())

        if not os.path.exists(src):
            errors.append({"file": src, "error": "Source file not found"})
            continue

        dest     = build_dest_path(output_root, artist, album, title, ext)
        dest     = _unique_path(dest)
        dest_dir = os.path.dirname(dest)

        try:
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
            shutil.move(src, dest)
            moved.append({"src": src, "dest": dest})

            if fetch_artwork and dest_dir not in artwork_done:
                cover_path = os.path.join(dest_dir, "cover.jpg")
                if not os.path.exists(cover_path):
                    mbid = get_release_mbid(artist, album)
                    fetch_cover_art(mbid, dest_dir)
                artwork_done.add(dest_dir)

        except Exception as e:
            errors.append({"file": src, "error": str(e)})

    return {"moved": len(moved), "errors": errors, "details": moved}


def preview_files(files: list[dict], output_root: str) -> list[dict]:
    previews = []
    for f in files:
        ext  = f.get("ext", Path(f.get("filename", "track.mp3")).suffix.lower())
        dest = build_dest_path(
            output_root,
            f.get("artist", "Unknown Artist"),
            f.get("album",  "Unknown Album"),
            f.get("title",  "track"),
            ext,
        )
        previews.append({"src": f["path"], "dest": dest})
    return previews
