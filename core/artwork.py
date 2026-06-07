import os
import requests
from pathlib import Path
from config import MUSICBRAINZ_USER_AGENT


def fetch_cover_art(mbid: str, dest_folder: str) -> bool:
    if not mbid:
        return False
    try:
        url = f"https://coverartarchive.org/release/{mbid}/front-500"
        r = requests.get(
            url,
            timeout=12,
            allow_redirects=True,
            headers={"User-Agent": MUSICBRAINZ_USER_AGENT},
        )
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
            Path(dest_folder).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(dest_folder, "cover.jpg"), "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False
