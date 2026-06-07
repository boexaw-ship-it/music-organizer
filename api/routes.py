import os
from flask import Blueprint, jsonify, request
from core.scanner import scan_folder
from core.musicbrainz import lookup_recording
from core.organizer import organize_files, preview_files
from api.errors import bad_request

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/scan", methods=["POST"])
def api_scan():
    folder = (request.json or {}).get("folder", "").strip()
    if not folder or not os.path.isdir(folder):
        return bad_request("Invalid or non-existent folder path")
    files = scan_folder(folder)
    return jsonify({"files": files, "count": len(files)})


@bp.route("/enrich", methods=["POST"])
def api_enrich():
    data   = request.json or {}
    artist = data.get("artist", "")
    title  = data.get("title",  "")
    result = lookup_recording(artist, title)
    return jsonify(result)


@bp.route("/preview", methods=["POST"])
def api_preview():
    data        = request.json or {}
    files       = data.get("files", [])
    output_root = data.get("output_root", "").strip()
    if not output_root:
        return bad_request("No output folder specified")
    previews = preview_files(files, output_root)
    return jsonify({"previews": previews})


@bp.route("/organize", methods=["POST"])
def api_organize():
    data          = request.json or {}
    files         = data.get("files", [])
    output_root   = data.get("output_root", "").strip()
    fetch_artwork = data.get("fetch_artwork", True)
    if not output_root:
        return bad_request("No output folder specified")
    result = organize_files(files, output_root, fetch_artwork)
    return jsonify(result)
