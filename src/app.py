from flask import Flask, jsonify

from app_v1.routes.main import app_v1
from config import config
from models import db
from v1.routes.anime import anime
from v1.routes.main import v1 as main
from v1.routes.scrapers import scrapers
from v1.routes.search import search


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(env)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


# environment = config['production']
environment = config['development']

app = create_app(environment)


@app.route('/')
def index():
    return jsonify(
        {'message': 'animethemes api', 'author': 'u/LetrixZ', 'docs': 'https://github.com/LetrixZ/animethemes-api'})


version = '/api/v1'
app.register_blueprint(main, url_prefix=version)

app.register_blueprint(anime, url_prefix=f'{version}/anime')
app.register_blueprint(anime, url_prefix=f'{version}/id')

app.register_blueprint(search, url_prefix=f'{version}/s')
app.register_blueprint(search, url_prefix=f'{version}/search')

app.register_blueprint(scrapers, url_prefix='/api/db')

app.register_blueprint(app_v1, url_prefix='/api/app/')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
