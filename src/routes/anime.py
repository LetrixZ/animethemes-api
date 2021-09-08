from flask import Blueprint, url_for, request
from werkzeug.utils import redirect
from db_models import Anime

anime = Blueprint('anime', __name__)


@anime.route('/get')
def get():
    mal_id = request.args.get('mal_id')
    return Anime.query.filter_by(mal_id=mal_id).first().json()


@anime.route('<int:anime_id>')
def get_anime(anime_id):
    entry = Anime.query.filter_by(mal_id=anime_id).first()
    if entry:
        return entry.json()
    else:
        return {'message': 'Item not found'}, 400


@anime.route('<int:anime_id>/<int:index>')
def redirect_theme(anime_id, index):
    return redirect(url_for('theme.get_theme', theme_id=f'{anime_id}-{index:02d}'))


@anime.route('<int:anime_id>/<int:index>/<int:quality>/audio')
def redirect_theme_audio(anime_id, index, quality):
    return redirect(url_for('theme.get_audio_theme', theme_id=f'{anime_id}-{index:02d}', quality=quality))
