from flask import Blueprint, jsonify, url_for
from werkzeug.utils import redirect

from src.data.repo import anime_list

anime = Blueprint('anime', __name__)


@anime.route('<int:anime_id>')
def get_anime(anime_id):
    entry = next((item for item in anime_list if item.anime_id == anime_id), None)
    if entry:
        return jsonify(entry.parse())
    else:
        return jsonify('Anime not found')


@anime.route('<int:anime_id>/<int:index>')
def redirect_theme(anime_id, index):
    return redirect(url_for('theme.get_theme', theme_id=f'{anime_id}-{index:02d}'))


@anime.route('<int:anime_id>/<int:index>/<int:quality>/audio')
def redirect_theme_audio(anime_id, index, quality):
    return redirect(url_for('theme.get_audio_theme', theme_id=f'{anime_id}-{index:02d}', quality=quality))
