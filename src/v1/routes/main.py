from flask import Blueprint, jsonify, request

from v1.helpers.anilist import get_anilist, filters as anilist_filters
from v1.helpers.myanimelist import get_mal_list, filters
from v1.helpers.search import *

v1 = Blueprint('v1', __name__)


@v1.route('stats')
def stats():
    return jsonify(
        {'anime count': Anime.query.count(), 'theme count': Theme.query.count(), 'artist count': Artist.query.count()})


@v1.route('')
def index():
    return jsonify(
        {'message': 'animethemes api', 'version': 'v1', 'author': 'u/LetrixZ',
         'docs': 'https://github.com/LetrixZ/animethemes-api'})


@v1.route('mal/<string:user>/<string:list_filter>')
@v1.route('mal/<string:user>')
def myanimelist_list(user, list_filter="all"):
    # CHECKING FOR FILTER
    status_query = request.args.get('status')
    if status_query:
        if int(status_query) in filters.values():
            return jsonify(get_mal_list(user, status_query))
        else:
            return jsonify({'available filters': filters})
    else:
        list_filter = list_filter.lower()
        if filters.get(list_filter):
            return jsonify(get_mal_list(user, filters[list_filter]))
        else:
            return jsonify({'available filters': filters})


@v1.route('anilist/<string:user>/<string:filter>')
@v1.route('anilist/<string:user>')
def anilist_list(user, filter=None):
    # API REQUEST
    ani_list = get_anilist(user, filter.upper())
    if not ani_list:
        return {'available filters': anilist_filters}
    # FILTERING
    anime_list = []
    for item in ani_list:
        mal_id = item['media']['idMal']
        anime = Anime.query.filter_by(mal_id=mal_id).first()
        if anime:
            anime_list.append(anime.json())
    anime_list = sorted(anime_list, key=lambda k: k['title'])
    return jsonify(anime_list)
