import random
from flask import Blueprint, jsonify, url_for
from werkzeug.utils import redirect

from src.data.repo import anime_list, artist_list, theme_list
from src.routes.seasons import list_years, list_current_season

android = Blueprint('android', __name__)


@android.route('years')
def get_year_list():
    return jsonify(list_years(True))


@android.route('home')
def get_home_list():
    return jsonify({'year_list': list_years(True), 'current_season': list_current_season(True),
                    # 'latest_anime': [item.app() for item in random.sample(anime_list, 6)],
                    # 'latest_artist': [item.app() for item in random.sample(artist_list, 6)]
                    })


@android.route('updates')
def get_updates():
    return jsonify(
        {'title': 'New version available!', 'message': 'This is a changelog', 'version': '1.0',
         'id': 1000})


@android.route('random')
def get_random_anime():
    return jsonify([item.app() for item in random.sample(anime_list, 15)])


@android.route('anime/<int:anime_id>')
def get_anime(anime_id):
    anime = next((item.app(True) for item in anime_list if item.anime_id == anime_id), None)
    return jsonify(anime)


@android.route('artist/<int:artist_id>')
def get_artist(artist_id):
    artist = next((item.parse() for item in artist_list if item.artist_id == artist_id), None)
    return jsonify(artist)


@android.route('theme/<string:theme_id>')
def get_theme(theme_id):
    theme = next((item.parse() for item in theme_list if item.theme_id == theme_id), None)
    return jsonify(theme)


@android.route('search/<path:name>')
def search_term(name):
    return jsonify({'anime_list': [item.app() for item in anime_list if name.lower() in item.title.lower()],
                    'theme_list': [item.parse(extended=True) for item in theme_list if
                                   name.lower() in item.title.lower()],
                    'artist_list': [item.app() for item in artist_list if name.lower() in item.name.lower()]})


@android.route('year/<int:year>')
def get_year(year):
    return redirect(url_for('season.list_year_season', year=year, app=True))


@android.route('mal/<string:user>')
def get_mal(user):
    return redirect(url_for('mal_list', user=user, app_r=True))


@android.route('anilist/<string:user>')
def get_anilist(user):
    return redirect(url_for('anilist_list', app_r=True, user=user))
