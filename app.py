import json

from flask import Flask, jsonify, request

from config import config
from routes.anime import anime, anime_list, parse_anime
from routes.artist import artist, parse_artist, artist_list
from routes.themes import theme, theme_list


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(env)
    return app


environment = config['production']

app = create_app(environment)

app.register_blueprint(anime, url_prefix='/a')
app.register_blueprint(anime, url_prefix='/anime')

app.register_blueprint(theme, url_prefix='/t')
app.register_blueprint(theme, url_prefix='/theme')

app.register_blueprint(artist, url_prefix='/artist')


@app.route('/s/anime/<path:name>')
def search_anime(name):
    return jsonify([parse_anime(item) for item in anime_list if name.lower() in item['title'].lower()])


@app.route('/s/artist/<path:name>')
def search_artist(name):
    return jsonify([parse_artist(item) for item in artist_list if name.lower() in item['name'].lower()])


@app.route('/s/theme/<path:name>')
def search_theme(name):
    return jsonify([item for item in theme_list if name.lower() in item['title'].lower()])


@app.route('/list/anime')
def list_anime():
    if request.args.get('parsed') == '1':
        tmp_list = [parse_anime(item) for item in anime_list]
        return jsonify(tmp_list)
    return jsonify(anime_list)


@app.route('/list/artist')
def list_artist():
    if request.args.get('parsed') == '1':
        tmp_list = [parse_artist(item) for item in artist_list]
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
