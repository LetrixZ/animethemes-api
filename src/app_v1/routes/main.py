from flask import Blueprint, jsonify
# from v1.helpers.others import *
from sqlalchemy import desc

from models import Anime, Artist, Theme
from v1.helpers.year_season import get_year_seasons

app_v1 = Blueprint('app_v1', __name__)


@app_v1.route('home')
def home_list():
    return jsonify({'year_list': get_year_list(), 'top_themes': top_themes(10), 'latest_anime': latest_anime(9),
                    'latest_themes': latest_themes(10), 'latest_artist': latest_artist(6)})


@app_v1.route('search/<path:term>')
def search(term):
    return jsonify(
        {'anime_list': search_anime(term), 'theme_list': search_theme(term), 'artist_list': search_artist(term)})


@app_v1.route('anime/<int:mal_id>')
def anime(mal_id):
    return Anime.query.filter_by(mal_id=mal_id).first().json()


@app_v1.route('artist/<int:mal_id>')
def artist(mal_id):
    return Artist.query.filter_by(mal_id=mal_id).first().app_detail_json()


@app_v1.route('theme/<string:theme_id>')
def theme(theme_id):
    return Theme.query.filter_by(theme_id=theme_id).first().json_info_extended()


@app_v1.route('year/<int:year>')
def year(year):
    return jsonify(get_year_seasons(year))


def latest_anime(limit):
    anime_list = Anime.query.order_by(Anime.id.desc()).limit(limit)
    result_list = []
    for anime in anime_list:
        result_list.append(anime.app_json())
    return result_list


def latest_artist(limit):
    artist_list = Artist.query.order_by(Artist.id.desc()).limit(limit)
    result_list = []
    for artist in artist_list:
        result_list.append(artist.app_json())
    return result_list


def latest_themes(limit):
    theme_list = Theme.query.order_by(Theme.id.desc()).limit(limit)
    result_list = []
    for theme in theme_list:
        result_list.append(theme.app_top_json())
    return result_list


def top_themes(limit):
    theme_list = Theme.query.order_by(Theme.views.desc()).limit(limit)
    result_list = []
    for theme in theme_list:
        result_list.append(theme.app_top_json())
    return result_list


def get_year_list():
    entries = Anime.query.order_by(desc(Anime.year)).all()
    year_list = set()
    for entry in entries:
        year_list.add(entry.year)
    year_list = list(year_list)
    year_list.sort(reverse=True)
    return year_list


def search_anime(name):
    results = Anime.query.all()
    anime_list = []
    for anime in results:
        if name.lower() in str(anime.title).lower():
            anime_list.append(anime.app_json())
    return anime_list


def search_theme(name):
    results = Theme.query.filter(Theme.title.ilike("%{}%".format(name))).all()
    theme_list = []
    for theme in results:
        theme_list.append(theme.app_top_json())
    return theme_list


def search_artist(name):
    results = Artist.query.filter(Artist.name.ilike("%{}%".format(name))).all()
    artist_list = []
    for artist in results:
        artist_list.append(artist.app_json())
    return artist_list
