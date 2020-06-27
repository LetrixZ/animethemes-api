from flask import Flask, jsonify
from config import config
from models import db, Anime
from scrapers import addYear, getUserList, getAllYears, getAllSeasons, getYearSeasons, getCurrentSeason, getSeason, getCoverFromDB
import json

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app

enviroment = config['development']

app = create_app(enviroment)

@app.route('/db/covers')
def getAllCovers():
    return jsonify(getAllCovers())

@app.route('/db/year/<string:year>')
def addYearToDB(year):
    animeList = addYear(year)
    for anime in animeList[0]:
        item = Anime.create(json.dumps(anime['titles']), anime['malId'], anime['cover'], anime['year'], anime['season'], json.dumps(anime['themes']))
    return jsonify(animeList[1])


@app.route('/api/v1/anime/<int:id>')
def getAnime(id):
    anime = Anime.query.filter_by(malId=id).first()
    return jsonify({'malId':anime.malId, 'title':json.loads(anime.title), 'cover':anime.cover, 'season':anime.season, 'year':anime.year, 'themes':json.loads(anime.themes)})

@app.route('/api/v1/search/<string:name>')
def searchAnime(name):
    term = '%{}%'.format(name)
    results = Anime.query.filter(Anime.title.ilike(term)).all()
    animeList = []
    for item in results:
        animeList.append(item.json())
    return jsonify(animeList)

@app.route('/api/v1/season/<string:year>/<string:season>')
def season(year, season):
    year = year.replace('s','')
    return jsonify(getSeason(year, season))

@app.route('/api/v1/seasons/<string:year>')
def yearSeasons(year):
    year = year.replace('s','')
    return jsonify(getYearSeasons(year))

@app.route('/api/v1/years')
def getYears():
    return jsonify(getAllYears())

@app.route('/api/v1/seasons')
def getSeasons():
    return jsonify(getAllSeasons())

@app.route('/api/v1/year/<string:year>')
def getYear(year):
    year = int(str(year).replace('s',''))
    results = Anime.query.filter_by(year=year).all()
    animeList = []
    for item in results:
        animeList.append(item.json())
    return jsonify(animeList)

@app.route('/api/v1/user/<string:user>')
def getMalList(user):
    userList = getUserList(user)
    return jsonify(userList)

@app.route('/api/v1/current')
def currentSeason():
    currentSeason, year = getCurrentSeason()
    print(currentSeason)
    print(year)
    return jsonify(getSeason(year, currentSeason))

if __name__ == '__main__':
    app.run()