from flask import Blueprint, jsonify

android = Blueprint('android', __name__)


@android.route('home')
def get_home_list():
    return jsonify({'year_list': get_year_list(), 'current_season': get_current_season(),
                    'latest_anime': latest_anime(9), 'latest_artist': latest_artist(6)})
