import random
from flask import Blueprint, jsonify

from src.data.repo import anime_list, artist_list
from src.routes.seasons import list_years, list_current_season

android = Blueprint('android', __name__)


@android.route('home')
def get_home_list():
    return jsonify({'year_list': list_years(True), 'current_season': list_current_season(True),
                    'latest_anime': [item.app() for item in random.sample(anime_list, 6)],
                    'latest_artist': [item.app() for item in random.sample(artist_list, 6)]})
