from flask import Blueprint, jsonify

# from v1.helpers.others import *
from models import Anime, Artist, Theme

app_v1 = Blueprint('app_v1', __name__)


@app_v1.route('home')
def home_list():
    return jsonify({'latest_anime': latest_anime(15)}, {'latest_themes': latest_themes(15)},
                   {'latest_artist': latest_artist(6)}, {'top_themes': top_themes(15)})


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
