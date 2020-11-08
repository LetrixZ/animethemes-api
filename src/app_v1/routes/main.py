import json
from difflib import SequenceMatcher

from flask import Blueprint, jsonify
# from v1.helpers.others import *
from sqlalchemy import desc

from models import Anime, Artist, Theme
from v1.helpers.anilist import get_anilist
from v1.helpers.myanimelist import get_bodies
from v1.helpers.year_season import get_year_seasons, get_current_season

app_v1 = Blueprint('app_v1', __name__)


@app_v1.route('home')
def home_list():
    # return jsonify({'year_list': get_year_list(), 'current_season': get_current_season(), 'top_themes': top_themes(10),
    #                 'latest_anime': latest_anime(9),
    #                 'latest_themes': latest_themes(10), 'latest_artist': latest_artist(6)})
    return jsonify({'year_list': get_year_list(), 'current_season': get_current_season(),
                    'latest_anime': latest_anime(9), 'latest_artist': latest_artist(6)})


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


# @app_v1.route('theme/<string:theme_id>')
# def theme(theme_id):
#     return Theme.query.filter_by(theme_id=theme_id).first().json_info_extended()


@app_v1.route('year/<int:year>')
def year(year):
    return jsonify(get_year_seasons(year))


@app_v1.route('mal/<string:user>')
def mal(user):
    # LIST REQUEST
    url_list = [f'https://myanimelist.net/animelist/{user}/load.json?offset={i}&status=7'
                for i in range(0, 300 * 10, 300)]
    bodies = get_bodies(url_list)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    mal_list = []
    # FILTERING
    for page in content:
        for entry in json.loads(page):
            if entry == 'errors':
                return {'error': 'user not found'}
            item = Anime.query.filter_by(mal_id=entry['anime_id']).first()
            if item:
                mal_list.append(item.app_json())
    mal_list = sorted(mal_list, key=lambda k: k['title'])
    return jsonify(mal_list)


@app_v1.route('anilist/<string:user>')
def anilist_list(user):
    # API REQUEST
    ani_list = get_anilist(user)
    # FILTERING
    anime_list = []
    for item in ani_list:
        mal_id = item['media']['idMal']
        item = Anime.query.filter_by(mal_id=mal_id).first()
        if item:
            anime_list.append(item.app_json())
    anime_list = sorted(anime_list, key=lambda k: k['title'])
    return jsonify(anime_list)


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


base_url = 'https://animethemes-api.herokuapp.com/api/v1/anime'


# def search_theme(name):
#     anime_list = Anime.query.all()
#     theme_list = []
#     for anime in anime_list:
#         for index, theme in enumerate(anime.themes):
#             if SequenceMatcher(a=theme['title'].lower(), b=name.lower()).ratio() > 0.8:
#                 theme['cover'] = anime.cover
#                 theme['name'] = anime.title[0]
#                 theme_list.append(theme)
#             elif name.lower() in theme['title'].lower() and theme['title'] != "":
#                 theme['cover'] = anime.cover
#                 theme['name'] = anime.title[0]
#                 theme_list.append(theme)
#             else:
#                 continue
#             mirror_list = []
#             for mirror_index, mirror in enumerate(theme['mirrors']):
#                 mirror['audio'] = f"{base_url}/{anime.mal_id}/{index}/{mirror_index}/audio"
#                 mirror['quality'] = ', '.join(mirror['quality'])
#                 mirror_list.append(mirror)
#             theme['mirrors'] = mirror_list
#     return theme_list

def search_theme(name):
    results = Theme.query.filter(Theme.title.ilike("%{}%".format(name))).all()
    theme_list = []
    for theme in results:
        theme_list.append(theme.json())
    return theme_list


def search_artist(name):
    results = Artist.query.filter(Artist.name.ilike("%{}%".format(name))).all()
    artist_list = []
    for artist in results:
        artist_list.append(artist.app_json())
    return artist_list
