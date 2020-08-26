from flask import Blueprint, jsonify

from v1.helpers.search import search_anime, search_theme, search_artist

search = Blueprint('search', __name__)


@search.route('<path:name>')
def search_all(name):
    return jsonify(
        {'anime_list': search_anime(name), 'theme_list': search_theme(name), 'artist_list': search_artist(name)})
