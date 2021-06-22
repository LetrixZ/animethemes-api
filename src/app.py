from flask import Flask, jsonify, request

from android.app import android
from config import config
from data.repo import artist_list, theme_list, anime_list
from helpers.anilist import get_anilist, filters as anilist_filters
from helpers.common import get_latest_data
from helpers.myanimelist import filters, get_mal_list
from routes.anime import anime
from routes.artist import artist
from routes.search import search
from routes.seasons import seasons
from routes.themes import theme


def create_app(env):
    flask_app = Flask(__name__)
    flask_app.config.from_object(env)
    return flask_app


environment = config['production']

app = create_app(environment)

app.register_blueprint(anime, url_prefix='/api/v1/anime')
app.register_blueprint(anime, url_prefix='/api/v1/a')
app.register_blueprint(anime, url_prefix='/api/v1/id')

app.register_blueprint(theme, url_prefix='/api/v1/theme')
app.register_blueprint(theme, url_prefix='/api/v1/t')

app.register_blueprint(artist, url_prefix='/api/v1/artist')

app.register_blueprint(search, url_prefix='/api/v1/search')
app.register_blueprint(search, url_prefix='/api/v1/s')

app.register_blueprint(seasons, url_prefix='/api/v1/season')

app.register_blueprint(android, url_prefix='/api/android')


@app.route('/api/v1/list/anime')
def list_anime():
    return jsonify([item.parse() for item in anime_list])


@app.route('/api/v1/list/artist')
def list_artist():
    return jsonify([item.parse() for item in artist_list])


@app.route('/api/v1/list/theme')
@app.route('/api/v1/list/themes')
def list_themes():
    return jsonify([item.parse() for item in theme_list])


@app.route('/api/v1/mal/<string:user>/<string:list_filter>')
@app.route('/api/v1/mal/<string:user>')
def mal_list(user, list_filter="all"):
    status_query = request.args.get('status')
    app_r = request.args.get('app_r')
    if status_query:
        if int(status_query) in filters.values():
            return jsonify(get_mal_list(user, status_query, app_r))
        else:
            return jsonify({'available filters': filters})
    else:
        list_filter = list_filter.lower()
        if filters.get(list_filter):
            return jsonify(get_mal_list(user, filters[list_filter], app_r))
        else:
            return jsonify({'available filters': filters})


@app.route('/api/v1/anilist/<string:user>/<string:filter>')
@app.route('/api/v1/anilist/<string:user>')
def anilist_list(user, list_filter=None):
    app_r = request.args.get('app_r')
    if list_filter:
        ani_list = get_anilist(user, list_filter.upper())
    else:
        ani_list = get_anilist(user)
    if not ani_list:
        return {'available filters': anilist_filters}
    a_list = []
    for item in ani_list:
        mal_id = item['media']['idMal']
        if app_r:
            entry = next((item.app() for item in anime_list if item.anime_id == mal_id), None)
        else:
            entry = next((item.parse() for item in anime_list if item.anime_id == mal_id), None)
        if entry:
            a_list.append(entry)
    a_list = sorted(a_list, key=lambda k: k['title'])
    return jsonify(a_list)


@app.route('/api/v1/latest')
def get_latest():
    return jsonify(get_latest_data())


@app.route('/api/v1/stats')
def get_stats():
    total_anime = len(anime_list)
    total_themes = len(theme_list)
    total_artist = len(artist_list)
    total_files = sum(len(item.mirrors) for item in theme_list)
    return jsonify({'total anime': total_anime, 'total themes': total_themes, 'total artists': total_artist,
                    'total files': total_files})


@app.route('/')
def index():
    return jsonify(
        {'message': 'animethemes api', 'author': 'Fermin Cirella (reddit: u/LetrixZ)',
         'docs': 'https://github.com/LetrixZ/animethemes-api'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
