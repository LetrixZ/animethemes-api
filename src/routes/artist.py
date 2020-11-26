from flask import Blueprint, jsonify

from src.data.repo import artist_list

artist = Blueprint('artist', __name__)


@artist.route('<int:artist_id>')
def get_artist(artist_id):
    entry = next((item for item in artist_list if item["artist_id"] == artist_id), None)
    if entry:
        return jsonify(entry.parse())
    else:
        return jsonify('Artist not found')
