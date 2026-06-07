# music.org

Local web tool for organizing music files into `Artist / Album / Song` folder structure.

Supports **MP3 · FLAC · WAV · M4A** with automatic metadata lookup via MusicBrainz.

---

## Features

- Reads ID3 / Vorbis / MP4 tags automatically
- Editable metadata table before any files are moved
- MusicBrainz lookup for missing artist / album / title (rate-limited: 1 req/s)
- Path preview before committing
- Album artwork download via Cover Art Archive (`cover.jpg` per album folder)
- Duplicate filename collision handling
- Output structure: `Artist / Album / Title.ext`

---

## Install

```bash
git clone https://github.com/you/music-organizer.git
cd music-organizer
pip install -r requirements.txt
```

Python 3.10+ required.

---

## Run

```bash
python app.py
```

Opens `http://127.0.0.1:5050` in your browser automatically.

---

## Folder structure

```
music-organizer/
├── app.py                  # Flask entry point
├── config.py               # Supported formats, settings
├── requirements.txt
├── .gitignore
├── core/
│   ├── scanner.py          # Walk folders, read tags (MP3/FLAC/WAV/M4A)
│   ├── organizer.py        # Move files, build paths, collision fix
│   ├── musicbrainz.py      # API lookup with rate limiting
│   └── artwork.py          # Cover art download
├── api/
│   ├── routes.py           # Flask blueprint: /scan /enrich /preview /organize
│   └── errors.py           # JSON error responses
└── templates/
    └── index.html          # Single-page Web UI
```

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/scan` | Scan a folder, return file list with tags |
| POST | `/api/enrich` | MusicBrainz lookup for one track |
| POST | `/api/preview` | Preview destination paths (no files moved) |
| POST | `/api/organize` | Move files and optionally download artwork |

---

## License

MIT
