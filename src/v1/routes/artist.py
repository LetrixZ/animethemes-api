from flask import Blueprint, jsonify
from models import Artist

artist = Blueprint('artist', __name__)


@artist.route('<int:mal_id>')
def get_artist(mal_id):
    artist_entry = Artist.query.filter_by(mal_id=mal_id).first()
    return jsonify(artist_entry.json())
