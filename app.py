import time
import json

from flask import Flask, jsonify

from config import config
from artist_scraper import get_list
from models import Artist, Theme, session, Anime
from anime_themes_scraper import get_year

anime_list = json.load(open('anime.json', 'r', encoding="utf8"))
theme_list = json.load(open('themes.json', 'r', encoding="utf8"))


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(env)
    return app


# environment = config['production']
environment = config['development']

app = create_app(environment)


def get_anime_themes():
    years = ['60s', '70s', '80s', '90s', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
             '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    added = {}
    for year in years:
        added[year] = get_year(year)
    print('Anime scrap successful')
    return added


def assign_artists():
    artist_list = session.query(Artist).all()
    for artist in artist_list:
        for theme in artist.themes:
            item = session.query(Theme).filter_by(theme_id=theme).first()
            try:
                item.artist_id = artist.mal_id
                item.save()
            except:
                return artist.name, theme
    return 'Artist assigment successfull'


def get_artists():
    if get_list():
        return 'Artist scrape successful'
    else:
        return 'Artist scrape unsuccessful'


timestamp = time.strftime("%Y%m%d-%H%M%S")


def save_anime():
    anime_db = session.query(Anime).all()
    anime_list = []
    for anime in anime_db:
        anime_list.append(anime.json_raw())
    with open('anime.json', 'w') as fp:
        json.dump(anime_list, fp)


def save_themes():
    theme_db = session.query(Theme).all()
    theme_list = []
    for theme in theme_db:
        theme_list.append(theme.json())
    with open('themes.json', 'w') as fp:
        json.dump(theme_list, fp)


@app.route('/s/anime/<path:name>')
def search_anime(name):
    return jsonify([item for item in anime_list if
                    name.lower() in item['title'].lower() or [synonym for synonym in item['synonyms'] if
                                                              name.lower() in synonym.lower()]])


@app.route('/s/theme/<path:name>')
def search_theme(name):
    return jsonify([item for item in theme_list if name.lower() in item['title'].lower()])


@app.route('/')
def index():
    return jsonify(
        {'message': 'animethemes api', 'author': 'Fermin Cirella (reddit: u/LetrixZ)',
         'docs': 'https://github.com/LetrixZ/animethemes-api'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
