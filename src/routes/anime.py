
from flask import Blueprint, jsonify

from src.data.repo import anime_list

anime = Blueprint('anime', __name__)


@anime.route('<int:anime_id>')
def get_anime(anime_id):
    entry = next((item for item in anime_list if item.anime_id == anime_id), None)
    if entry:
        return jsonify(entry.parse())
    else:
        return jsonify('Anime not found')


