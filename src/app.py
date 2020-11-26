from flask import Flask, jsonify, request

from src.config import config
from src.data.repo import artist_list, theme_list, anime_list
from src.routes.anime import anime
from src.routes.artist import artist
from src.routes.search import search
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


@app.route('/')
def index():
    return jsonify(
        {'message': 'animethemes api', 'author': 'Fermin Cirella (reddit: u/LetrixZ)',
         'docs': 'https://github.com/LetrixZ/animethemes-api-lite'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
