from flask import Flask, jsonify, request

from src.config import config
from src.data.repo import artist_list, theme_list, anime_list
from src.helpers.anilist import get_anilist, filters as anilist_filters
from src.helpers.myanimelist import filters, get_mal_list
from src.routes.anime import anime
from src.routes.artist import artist
from src.routes.search import search
from src.routes.seasons import seasons
from src.routes.themes import theme


def create_app(env):
    flask_app = Flask(__name__)
    flask_app.config.from_object(env)
    return flask_app


environment = config['development']

app = create_app(environment)

app.register_blueprint(anime, url_prefix='/a')
app.register_blueprint(anime, url_prefix='/anime')

app.register_blueprint(theme, url_prefix='/t')
app.register_blueprint(theme, url_prefix='/theme')

app.register_blueprint(artist, url_prefix='/artist')

app.register_blueprint(search, url_prefix='/s')
app.register_blueprint(search, url_prefix='/search')

app.register_blueprint(seasons, url_prefix='/season')


@app.route('/list/anime')
def list_anime():
    if request.args.get('parsed') == '1':
        tmp_list = [item.parse() for item in anime_list]
        return jsonify(tmp_list)
    return jsonify(anime_list)


@app.route('/list/artist')
def list_artist():
    if request.args.get('parsed') == '1':
        tmp_list = [item.parse() for item in artist_list]
        return jsonify(tmp_list)
    return jsonify(artist_list)


@app.route('/list/themes')
def list_themes():
    return jsonify(theme_list)


@app.route('/mal/<string:user>/<string:list_filter>')
@app.route('/mal/<string:user>')
def mal_list(user, list_filter="all"):
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


@app.route('/anilist/<string:user>/<string:filter>')
@app.route('/anilist/<string:user>')
def anilist_list(user, filter=None):
    # API REQUEST
    if filter:
        ani_list = get_anilist(user, filter.upper())
    else:
        ani_list = get_anilist(user)
    if not ani_list:
        return {'available filters': anilist_filters}
    # FILTERING
    a_list = []
    for item in ani_list:
        mal_id = item['media']['idMal']
        entry = next((item.parse() for item in anime_list if item.anime_id == mal_id), None)
        if entry:
            a_list.append(entry)
    a_list = sorted(a_list, key=lambda k: k.title)
    return jsonify(a_list)


@app.route('/')
def index():
    return jsonify(
        {'message': 'animethemes api', 'author': 'Fermin Cirella (reddit: u/LetrixZ)',
         'docs': 'https://github.com/LetrixZ/animethemes-api-lite'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
