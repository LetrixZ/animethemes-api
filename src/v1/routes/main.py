from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from v1.helpers.anilist import get_anilist, filters as anilist_filters
from v1.helpers.myanimelist import get_mal_list, filters
from v1.helpers.others import *
from v1.helpers.search import *
from v1.helpers.year_season import get_all_seasons, get_year_seasons, get_season, get_current_season

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
    if filter:
        ani_list = get_anilist(user, filter.upper())
    else:
        ani_list = get_anilist(user)
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


@v1.route('year/<int:year>')
@v1.route('year/')
def get_year(year=None):
    if year:
        entries = Anime.query.filter_by(year=year).all()
        return jsonify([anime.json() for anime in entries])
    else:
        entries = Anime.query.order_by(desc(Anime.year)).all()
        year_list = set()
        for entry in entries:
            year_list.add(entry.year)
        year_list = list(year_list)
        year_list.reverse()
        return jsonify(year_list)


@v1.route('seasons/<int:year>')
@v1.route('seasons/')
def season_api(year=None):
    current = True if request.args.get('current') == "1" else False
    season = request.args.get('season')
    if current:
        return jsonify(get_current_season())
    elif year and season:
        return jsonify(get_season(year, season))
    elif year and not season:
        return jsonify(get_year_seasons(year))
    else:
        return jsonify(get_all_seasons())


@v1.route('latest')
def latest_api():
    limit = request.args.get('limit', 20)
    type = request.args.get('type', 'anime')
    if type == 'anime':
        return jsonify(latest_anime(limit))
    elif type == 'theme':
        return jsonify(latest_themes(limit))
    elif type == 'artist':
        return jsonify(latest_artist(limit))
    else:
        return jsonify({'error': 'invalid type'})


@v1.route('latest/animes')
def get_latest_anime():
    limit = 20
    return jsonify(latest_anime(limit))


@v1.route('latest/themes')
def get_latest_themes():
    limit = 20
    return jsonify(latest_themes(limit))


@v1.route('top')
def top():
    limit = request.args.get('limit', 20)
    return jsonify(top_themes(limit))


@v1.route('list/anime')
def get_all_anime():
    return jsonify(all_anime())


@v1.route('list/theme')
def get_all_themes():
    return jsonify(all_theme())


@v1.route('list/anime/<int:page>')
def get_anime(page):
    return jsonify(all_anime_page(page))


@v1.route('list/theme/<int:page>')
def get_themes(page):
    return jsonify(all_themes_page(page))
