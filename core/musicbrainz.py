import time
import requests
from config import MUSICBRAINZ_RATE_LIMIT, MUSICBRAINZ_USER_AGENT

_last_request_time = 0.0


def _throttle():
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    if elapsed < MUSICBRAINZ_RATE_LIMIT:
        time.sleep(MUSICBRAINZ_RATE_LIMIT - elapsed)
    _last_request_time = time.monotonic()


def _get(url: str, params: dict) -> dict:
    _throttle()
    try:
        r = requests.get(
            url,
            params=params,
            headers={"User-Agent": MUSICBRAINZ_USER_AGENT},
            timeout=8,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


def lookup_recording(artist: str, title: str) -> dict:
    result = {"artist": artist, "album": "", "title": title}

    query_parts = []
    if artist and artist != "Unknown Artist":
        query_parts.append(f'artist:"{artist}"')
    if title and title != "Unknown":
        query_parts.append(f'recording:"{title}"')
    if not query_parts:
        return result

    data = _get(
        "https://musicbrainz.org/ws/2/recording/",
        {"query": " AND ".join(query_parts), "fmt": "json", "limit": 1},
    )
    recordings = data.get("recordings", [])
    if not recordings:
        return result

    rec = recordings[0]
    result["title"] = rec.get("title", title)
    credits = rec.get("artist-credit", [])
    if credits:
        result["artist"] = credits[0].get("artist", {}).get("name", artist)
    releases = rec.get("releases", [])
    if releases:
        result["album"] = releases[0].get("title", "")

    return result


def get_release_mbid(artist: str, album: str) -> str:
    if not (artist and album):
        return ""
    data = _get(
        "https://musicbrainz.org/ws/2/release/",
        {
            "query": f'artist:"{artist}" AND release:"{album}"',
            "fmt": "json",
            "limit": 1,
        },
    )
    releases = data.get("releases", [])
    if releases:
        return releases[0].get("id", "")
    return ""
