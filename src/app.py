import concurrent
import json
import random
import string
import subprocess

import fileioapi as fileioapi
import requests
from flask import Flask, jsonify, request
from src.config import config
from src.models import db, Anime, User, Playlist
from src.anilist import getListFromUser
from flask_apidoc_extend import ApiDoc
from src.audio_scraper import get_audio, get_audio_name, get_audio_anime, get_music
from src.scrapersv2 import get_year as v2_get_year
from src.scrapers import add_year, getUserList, getAllYears, getAllSeasons, getYearSeasons, getCurrentSeason, getSeason, \
    getCoverFromDB
from werkzeug.utils import redirect
from difflib import SequenceMatcher


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environment)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


environment = config['production']
# environment = config['development']

app = create_app(environment)
ApiDoc(app=app)


def random_string(stringLength=8):
    letters = string.ascii_lowercase + "123456789" + string.ascii_lowercase.upper()
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_user(name, password):
    return User.create(name.lower(), password)


@app.route('/playlist/login', methods=['POST'])
def login():
    content = request.get_json()
    username = content.get("username")
    password = content.get("password")
    user = User.query.filter_by(username=username.lower()).first()
    if user is not None:
        if password == user.password:
            print("Login successful")
            response = user.json()
            response['message'] = "successful"
            return jsonify(response)
        else:
            print("Bad user")
            response = {'username': username, 'password': password, 'playId': None, 'message': "bad_user"}
            return jsonify(response)
    else:
        print("Not found")
        new_user = create_user(username, password)
        response = new_user.json()
        response['message'] = "not_found"
        return jsonify(response)


@app.route('/playlist/set', methods=['POST'])
def set_play_id():
    content = request.get_json()
    username = content.get("username")
    password = content.get("password")
    playId = content.get("playId")
    user = User.query.filter_by(username=username).first()
    if user:
        if password == user.password:
            user.playId = playId
            user.update()
            return jsonify({'message': 'playId set successful'})


@app.route('/playlist/upload', methods=['POST'])
def save_playlist():
    content = request.get_json()
    playlists = content.get('collection')
    playId = content.get('playId')
    actualPlaylist = content.get('actual_pos')
    row = Playlist.query.filter_by(playId=playId).first()
    if row:
        row.playlists = json.dumps(playlists)
        row.actualPlaylist = actualPlaylist
        row.update()
    return jsonify({'message': "{} saved succesfully".format(playId)})


# AUDIO
@app.route('/api/v1/audio/<string:name>')
def search_audio(name):
    audio_list = get_audio(name, None)
    return jsonify(audio_list)


# @app.route('/db/audio/')
# def add_audio():
#     anime_list = Anime.query.all()
#     added = []
#     for anime in anime_list:
#         print(json.loads(anime.title)[0])
#         themes = json.loads(anime.themes)
#         for theme in themes:
#             if not theme.get('audio'):
#                 print("{} missing ({})".format(theme.get('title'), json.loads(anime.title)[0]))
#                 audio = get_audio(theme.get('title'), anime)
#                 titles = json.loads(anime.title)
#                 for entry in audio:
#                     for title in titles:
#                         # if entry.get('anime') == title:
#                         if SequenceMatcher(a=entry.get('anime'), b=title).ratio() > 0.9:
#                             theme['audio'] = entry
#                             break
#         anime.themes = json.dumps(themes)
#         db.session.commit()
#         added.append(anime.json())
#     return jsonify(added)

@app.route('/db/audio/')
def add_audio():
    anime_list = Anime.query.all()
    for anime in anime_list:
        anime_title = json.loads(anime.title)[0]
        themes = json.loads(anime.themes)
        for theme in themes:
            if theme.get("audio"):
                continue
            print("{} missing ({})".format(theme.get('title'), anime_title))
            audio = get_audio_name(theme, anime)
            if audio is not None:
                theme["audio"] = audio
            else:
                theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
        anime.themes = json.dumps(themes)
        db.session.commit()
    return jsonify({'message': 'done'})


@app.route('/db/audio2/')
def add_audio_2():
    anime_list = Anime.query.all()
    for anime in anime_list:
        if len(json.loads(anime.title)[0]) > 3:
            themes = json.loads(anime.themes)
            for theme in themes:
                print(theme.get('audio'))
                if not theme.get('audio'):
                    item = get_audio_anime(anime)
                    anime.themes = json.dumps(item)
                    # db.session.commit()
                    break
                    # print(item)
    return jsonify({'message': 'done'})


@app.route('/music')
def add_music():
    anime_list = Anime.query.all()
    for anime in anime_list:
        anime_title = json.loads(anime.title)[0]
        if len(anime_title) >= 3:
            themes = json.loads(anime.themes)
            for theme in themes:
                if not theme.get('audio'):
                    item = get_music(anime)
                    anime.themes = json.dumps(item)
                    db.session.commit()
                    break
    return jsonify({'message': 'done'})


# GET PLAYLIST COLLECTION
@app.route('/playlist/get', methods=['POST'])
def get_playlists():
    content = request.get_json()
    playId = content.get('message')
    row = Playlist.query.filter_by(playId=playId).first()
    if not row:
        return jsonify(None)
    playlist = row.json()
    return jsonify(playlist)


@app.route('/playlist/generate')
def create_playid():
    playId = random_string(6)
    while Playlist.query.filter_by(playId=playId).first() is not None:
        playId = random_string(6)
    Playlist.create(playId)
    return jsonify({'message': playId})


@app.route('/db/covers')
def get_all_covers():
    return jsonify(getCoverFromDB())


@app.route('/db/year/<string:year>')
def add_year_to_db(year):
    animeList = add_year(year)
    for anime in animeList[0]:
        Anime.create(json.dumps(anime['titles']), anime['malId'], anime['cover'], anime['year'], anime['season'],
                     json.dumps(anime['themes']))
    return jsonify(animeList[1])


@app.route('/add/<string:year>')
def add_year(year):
    anime_list = v2_get_year(year)
    for season_list in anime_list:
        for anime in season_list:
            Anime.create(json.dumps(anime['titles']), anime['malId'], anime['cover'], anime['year'], anime['season'],
                         json.dumps(anime['themes']))
    return jsonify(anime_list)


@app.route('/api/v1/anilist/<string:user>')
def get_anilist(user):
    """
        @api {get} /anilist/:anilist_user Request AniList's user list
        @apiName get_anilist
        @apiGroup User

        @apiParam {String} mal_user AniList's username

        @apiSuccess {int} malId MyAnimeList's id for the anime
        @apiSuccess {String[]} title Title and synonims of the anime
        @apiSuccess {String} cover URL of the anime cover
        @apiSuccess {String} season Season of the anime
        @apiSuccess {int} year Year of the anime
        @apiSuccess {Object[]} themes List of themes
        @apiSuccess {String} themes.title Title of the theme
        @apiSuccess {String} themes.type Type of the theme
        @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
        @apiSuccess {String} themes.mirror.quality Quality of the mirror
        @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} themes.episodes Episodes of the theme
        @apiSuccess {String} themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            [
                ...
                {
                  "malId":40060,
                  "title":[
                     "BNA",
                     "Brand New Animal"
                  ],
                  "cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
                  "season":"Spring 2020",
                  "year":2020,
                  "themes":[
                     {
                        "title":"Ready to",
                        "type":"OP V1",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1.webm"
                           }
                        ],
                        "episodes":"1-5",
                        "notes":""
                     },
                     {
                        "title":"Ready to",
                        "type":"OP V2",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm"
                           }
                        ],
                        "episodes":"6-11",
                        "notes":""
                     },
                     ...
                  ]
               },
               ...
           ]
        """
    aniList = getListFromUser(user)
    animeList = []
    for item in aniList:
        malId = item['media']['idMal']
        anime = Anime.query.filter_by(malId=malId).first()
        if anime:
            animeList.append(
                {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
                 'year': anime.year, 'themes': json.loads(anime.themes)})
    animeList = sorted(animeList, key=lambda k: k['title'])
    return jsonify(animeList)


@app.route('/api/v1/anime/<int:malId>')
def get_anime(malId):
    """
        @api {get} /anime/:mal_id Request anime and themes with MyAnimeList's anime id
        @apiName get_anime
        @apiGroup Anime

        @apiParam {int} mal_id MyAnimeList's anime id

        @apiSuccess {int} malId MyAnimeList's id for the anime
        @apiSuccess {String[]} title Title and synonims of the anime
        @apiSuccess {String} cover URL of the anime cover
        @apiSuccess {String} season Season of the anime
        @apiSuccess {int} year Year of the anime
        @apiSuccess {Object[]} themes List of themes
        @apiSuccess {String} themes.title Title of the theme
        @apiSuccess {String} themes.type Type of the theme
        @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
        @apiSuccess {String} themes.mirror.quality Quality of the mirror
        @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} themes.episodes Episodes of the theme
        @apiSuccess {String} themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            {
               "malId":13601,
               "title":[
                  "Psycho Pass",
                  "Psychopath"
               ],
               "cover":"https://cdn.myanimelist.net/images/anime/5/43399.jpg",
               "season":"Fall 2012",
               "year":2012,
               "themes":[
                  {
                     "title":"abnormalize",
                     "type":"OP1",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-OP1.webm"
                        }
                     ],
                     "episodes":"1-11",
                     "notes":""
                  },
                  {
                     "title":"Out of Control",
                     "type":"OP2 V1",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-OP2v2.webm"
                        }
                     ],
                     "episodes":"12",
                     "notes":""
                  },
                  {
                     "title":"Out of Control",
                     "type":"OP2 V2",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-OP2.webm"
                        }
                     ],
                     "episodes":"13-22",
                     "notes":""
                  },
                  {
                     "title":"Namae no nai Kaibutsu",
                     "type":"ED1 V1",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-ED1.webm"
                        }
                     ],
                     "episodes":"1-3, 5, 7-8, 10-11",
                     "notes":""
                  },
                  {
                     "title":"Namae no nai Kaibutsu",
                     "type":"ED1 V2",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-ED1v2.webm"
                        }
                     ],
                     "episodes":"4, 6, 9",
                     "notes":""
                  },
                  {
                     "title":"All Alone With You",
                     "type":"ED2 V1",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-ED2.webm"
                        }
                     ],
                     "episodes":"12-21",
                     "notes":""
                  },
                  {
                     "title":"All Alone With You",
                     "type":"ED2 V2",
                     "mirror":[
                        {
                           "quality":"NC, BD, 1080, Over",
                           "mirrorUrl":"https://animethemes.moe/video/PsychoPass-ED2v2.webm"
                        }
                     ],
                     "episodes":"22",
                     "notes":"Spoiler"
                  }
               ]
            }
        """
    anime = Anime.query.filter_by(malId=malId).first()
    if anime:
        themes = json.loads(anime.themes)
        for theme in themes:
            if not theme.get('audio'):
                print("{} missing".format(theme.get('title')))
                audio = get_audio(theme.get('title'), anime)
                titles = json.loads(anime.title)
                for entry in audio:
                    for title in titles:
                        if entry.get('anime') == title.replace("'", ""):
                            theme['audio'] = entry
                            break
            anime.themes = json.dumps(themes)
            db.session.commit()
        return jsonify(
            {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': themes})
    else:
        return jsonify({'message': 'not found'})


@app.route('/api/v1/search/<string:name>')
def search_anime(name):
    """
        @api {get} /search/:search_term Perform a search on the DB to check for results based on search term
        @apiName search_anime
        @apiGroup Anime

        @apiParam {String} search_term Search term

        @apiSuccess {int} malId MyAnimeList's id for the anime
        @apiSuccess {String[]} title Title and synonims of the anime
        @apiSuccess {String} cover URL of the anime cover
        @apiSuccess {String} season Season of the anime
        @apiSuccess {int} year Year of the anime
        @apiSuccess {Object[]} themes List of themes
        @apiSuccess {String} themes.title Title of the theme
        @apiSuccess {String} themes.type Type of the theme
        @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
        @apiSuccess {String} themes.mirror.quality Quality of the mirror
        @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} themes.episodes Episodes of the theme
        @apiSuccess {String} themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            [
                ...
                {
                  "malId":40060,
                  "title":[
                     "BNA",
                     "Brand New Animal"
                  ],
                  "cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
                  "season":"Spring 2020",
                  "year":2020,
                  "themes":[
                     {
                        "title":"Ready to",
                        "type":"OP V1",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1.webm"
                           }
                        ],
                        "episodes":"1-5",
                        "notes":""
                     },
                     {
                        "title":"Ready to",
                        "type":"OP V2",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm"
                           }
                        ],
                        "episodes":"6-11",
                        "notes":""
                     },
                     ...
                  ]
               },
               ...
           ]
        """
    term = '%{}%'.format(name)
    results = Anime.query.filter(Anime.title.ilike(term)).all()
    animeList = []
    for item in results:
        animeList.append(item.json())
    return jsonify(animeList)


@app.route('/api/v1/season/<string:year>/<string:season>')
def season(year, season):
    """
        @api {get} /season/:year/:season Request list of anime and themes based on year and season
        @apiName season
        @apiGroup Anime

        @apiParam {int} year Year
        @apiParam {String} season Season

        @apiSuccess {int} malId MyAnimeList's id for the anime
        @apiSuccess {String[]} title Title and synonims of the anime
        @apiSuccess {String} cover URL of the anime cover
        @apiSuccess {String} season Season of the anime
        @apiSuccess {int} year Year of the anime
        @apiSuccess {Object[]} themes List of themes
        @apiSuccess {String} themes.title Title of the theme
        @apiSuccess {String} themes.type Type of the theme
        @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
        @apiSuccess {String} themes.mirror.quality Quality of the mirror
        @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} themes.episodes Episodes of the theme
        @apiSuccess {String} themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            [
                ...
                {
                  "malId":40060,
                  "title":[
                     "BNA",
                     "Brand New Animal"
                  ],
                  "cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
                  "season":"Spring 2020",
                  "year":2020,
                  "themes":[
                     {
                        "title":"Ready to",
                        "type":"OP V1",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1.webm"
                           }
                        ],
                        "episodes":"1-5",
                        "notes":""
                     },
                     {
                        "title":"Ready to",
                        "type":"OP V2",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm"
                           }
                        ],
                        "episodes":"6-11",
                        "notes":""
                     },
                     ...
                  ]
               },
               ...
           ]
        """
    year = year.replace('s', '')
    return jsonify(getSeason(year, season))


@app.route('/api/v1/seasons/<string:year>')
def year_seasons(year):
    """
        @api {get} /seasons/:year/ Request list of seasons based on year
        @apiName year_seasons
        @apiGroup Anime

        @apiParam {int} year Year

        @apiSuccess {String} year Year
        @apiSuccess {Object[]} seasons Seasons of the year
        @apiSuccess {String} seasons.season Season of the year
        @apiSuccess {Object[]} seasons.animes List of animes of the season
        @apiSuccess {int} seasons.animes.malId MyAnimeList's id for the anime
        @apiSuccess {String[]} seasons.animes.title Title and synonims of the anime
        @apiSuccess {String} seasons.animes.cover URL of the anime cover
        @apiSuccess {String} seasons.animes.season Season of the anime
        @apiSuccess {int} seasons.animes.year Year of the anime
        @apiSuccess {Object[]} seasons.animes.themes List of themes
        @apiSuccess {String} seasons.animes.themes.title Title of the theme
        @apiSuccess {String} seasons.animes.themes.type Type of the theme
        @apiSuccess {Object[]} seasons.animes.themes.mirror List of mirrors for the theme
        @apiSuccess {String} seasons.animes.themes.mirror.quality Quality of the mirror
        @apiSuccess {String} seasons.animes.themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} seasons.animes.themes.episodes Episodes of the theme
        @apiSuccess {String} seasons.animes.themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            {
               "year":"2000",
               "seasons":[
                  {
                     "season":"Fall",
                     "animes":[
                        {
                           "malId":1281,
                           "title":[
                              "Gakkou no Kaidan",
                              "Ghost Stories"
                           ],
                           "cover":"https://cdn.myanimelist.net/images/anime/9/18360.jpg",
                           "season":"Fall 2000",
                           "year":2000,
                           "themes":[
                              {
                                 "title":"Grow Up",
                                 "type":"OP",
                                 "mirror":[
                                    {
                                       "quality":"NC, DVD, 480",
                                       "mirrorUrl":"https://animethemes.moe/video/GakkouNoKaidan-OP1.webm"
                                    }
                                 ],
                                 "episodes":"",
                                 "notes":""
                              },
                              {
                                 "title":"sexy sexy",
                                 "type":"ED",
                                 "mirror":[
                                    {
                                       "quality":"NC, DVD, 480",
                                       "mirrorUrl":"https://animethemes.moe/video/GakkouNoKaidan-ED1.webm"
                                    }
                                 ],
                                 "episodes":"",
                                 "notes":""
                              }
                           ]
                        },
                        ...
                     ]
                  },
                  ...
              ]
            }
        """
    year = year.replace('s', '')
    return jsonify(getYearSeasons(year))


@app.route('/api/v1/years')
def get_years():
    """
        @api {get} /years Request list of years available on the DB
        @apiName get_years
        @apiGroup Data

        @apiSuccess {String[]} years List years

        @apiSuccessExample {json} Success-Response:
            [2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,90,80,70,60]
    """
    return jsonify(getAllYears())


@app.route('/api/v1/seasons')
def get_seasons():
    """
        @api {get} /years Request list of years available on the DB
        @apiName get_seasons
        @apiGroup Data

        @apiSuccess {Object[]} years List years and seasons
        @apiSuccess {String} years.year Year
        @apiSuccess {String[]} year.seasons Seasons of the year

        @apiSuccessExample {json} Success-Response:
            [
               {
                  "year":2020,
                  "seasons":[
                     "Spring",
                     "Winter"
                  ]
               },
               {
                  "year":2019,
                  "seasons":[
                     "Fall",
                     "Summer",
                     "Spring",
                     "Winter"
                  ]
               },
               {
                  "year":2018,
                  "seasons":[
                     "Spring",
                     "Fall",
                     "Summer",
                     "Winter"
                  ]
               },
               ...
           ]
    """
    return jsonify(getAllSeasons())


@app.route('/api/v1/year/<string:year>')
def get_year(year):
    """
        @api {get} /year/:year Request list of anime and themes of the year
        @apiName get_year
        @apiGroup Anime

        @apiParam {int} year Year

        @apiSuccess {int} malId MyAnimeList's id for the anime
        @apiSuccess {String[]} title Title and synonims of the anime
        @apiSuccess {String} cover URL of the anime cover
        @apiSuccess {String} season Season of the anime
        @apiSuccess {int} year Year of the anime
        @apiSuccess {Object[]} themes List of themes
        @apiSuccess {String} themes.title Title of the theme
        @apiSuccess {String} themes.type Type of the theme
        @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
        @apiSuccess {String} themes.mirror.quality Quality of the mirror
        @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} themes.episodes Episodes of the theme
        @apiSuccess {String} themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            [
                ...
                {
                  "malId":40060,
                  "title":[
                     "BNA",
                     "Brand New Animal"
                  ],
                  "cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
                  "season":"Spring 2020",
                  "year":2020,
                  "themes":[
                     {
                        "title":"Ready to",
                        "type":"OP V1",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1.webm"
                           }
                        ],
                        "episodes":"1-5",
                        "notes":""
                     },
                     {
                        "title":"Ready to",
                        "type":"OP V2",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm"
                           }
                        ],
                        "episodes":"6-11",
                        "notes":""
                     },
                     ...
                  ]
               },
               ...
           ]
    """
    year = int(str(year).replace('s', ''))
    results = Anime.query.filter_by(year=year).all()
    animeList = []
    for item in results:
        animeList.append(item.json())
    return jsonify(animeList)


@app.route('/api/v1/user/<string:user>')
def get_mal_list(user):
    """
    @api {get} /user/:mal_user Request MyAnimeList's user list
    @apiName get_mal_list
    @apiGroup User

    @apiParam {String} mal_user MyAnimeList's username

    @apiSuccess {int} malId MyAnimeList's id for the anime
    @apiSuccess {String[]} title Title and synonims of the anime
    @apiSuccess {String} cover URL of the anime cover
    @apiSuccess {String} season Season of the anime
    @apiSuccess {int} year Year of the anime
    @apiSuccess {Object[]} themes List of themes
    @apiSuccess {String} themes.title Title of the theme
    @apiSuccess {String} themes.type Type of the theme
    @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
    @apiSuccess {String} themes.mirror.quality Quality of the mirror
    @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
    @apiSuccess {String} themes.episodes Episodes of the theme
    @apiSuccess {String} themes.notes Notes of the theme

    @apiSuccessExample {json} Success-Response:
        [
            ...
            {
              "malId":40060,
              "title":[
                 "BNA",
                 "Brand New Animal"
              ],
              "cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
              "season":"Spring 2020",
              "year":2020,
              "themes":[
                 {
                    "title":"Ready to",
                    "type":"OP V1",
                    "mirror":[
                       {
                          "quality":"default",
                          "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1.webm"
                       }
                    ],
                    "episodes":"1-5",
                    "notes":""
                 },
                 {
                    "title":"Ready to",
                    "type":"OP V2",
                    "mirror":[
                       {
                          "quality":"default",
                          "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm"
                       }
                    ],
                    "episodes":"6-11",
                    "notes":""
                 },
                 ...
              ]
           },
           ...
       ]
    """
    userList = getUserList(user)
    return jsonify(userList)


@app.route('/api/v1/current')
def current_season():
    """
        @api {get} /current Request list of anime and themes of the current season
        @apiName current_season
        @apiGroup Anime

        @apiSuccess {int} malId MyAnimeList's id for the anime
        @apiSuccess {String[]} title Title and synonims of the anime
        @apiSuccess {String} cover URL of the anime cover
        @apiSuccess {String} season Season of the anime
        @apiSuccess {int} year Year of the anime
        @apiSuccess {Object[]} themes List of themes
        @apiSuccess {String} themes.title Title of the theme
        @apiSuccess {String} themes.type Type of the theme
        @apiSuccess {Object[]} themes.mirror List of mirrors for the theme
        @apiSuccess {String} themes.mirror.quality Quality of the mirror
        @apiSuccess {String} themes.mirror.mirrorUrl URL of the mirror
        @apiSuccess {String} themes.episodes Episodes of the theme
        @apiSuccess {String} themes.notes Notes of the theme

        @apiSuccessExample {json} Success-Response:
            [
                ...
                {
                  "malId":40060,
                  "title":[
                     "BNA",
                     "Brand New Animal"
                  ],
                  "cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
                  "season":"Spring 2020",
                  "year":2020,
                  "themes":[
                     {
                        "title":"Ready to",
                        "type":"OP V1",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1.webm"
                           }
                        ],
                        "episodes":"1-5",
                        "notes":""
                     },
                     {
                        "title":"Ready to",
                        "type":"OP V2",
                        "mirror":[
                           {
                              "quality":"default",
                              "mirrorUrl":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm"
                           }
                        ],
                        "episodes":"6-11",
                        "notes":""
                     },
                     ...
                  ]
               },
               ...
           ]
    """
    current_season, year = getCurrentSeason()
    return jsonify(getSeason(year, "Summer"))


@app.route('/api/v1/latest')
def latest_themes():
    animes = Anime.query.order_by(Anime.id.desc()).limit(15)
    animeList = []
    for anime in animes:
        # themes = json.loads(anime.themes)
        # for theme in themes:
        #     print(theme.get('title'))
        #     audio = get_audio(theme.get('title'))
        #     theme['audio'] = audio[0]
        animeList.append(
            {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': json.loads(anime.themes)})
        # animeList.append(
        #     {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
        #      'year': anime.year, 'themes': themes})
    return jsonify(animeList)


@app.route('/api/v1/anime/<int:malId>/<int:theme>/<int:version>')
def getTheme(malId, theme, version):
    anime = Anime.query.filter_by(malId=malId).first()
    if anime:
        themes = json.loads(anime.themes)
        try:
            url = themes[theme].get('mirror')[version]
            themes[theme].get('extras')['views'] += 1
            anime.themes = json.dumps(themes)
            anime.update()
            return jsonify({'message': themes[theme].get('extras')['views']})
            # print(themes[theme].get('extras')['views'])
            # return redirect(url.get('mirrorUrl'))
        except IndexError:
            return jsonify({'message': 'bad index'})
        # try:
        #     themeItem = json.loads(anime.themes)[theme]
        #     try:
        #         versionItem = themeItem.get('mirror')[version]
        #         extras = themeItem.get('extras')
        #         views = extras.get('views') + 1
        #         extras['views'] = views
        #         themeItem['extras'] = extras
        #         anime.update()
        #         print(views)
        #         return redirect(versionItem.get('mirrorUrl'))
        #     except IndexError:
        #         return jsonify({'message': len(themeItem.get('mirror'))})
        # except IndexError:
        #     return jsonify({'message': len(json.loads(anime.themes))})


@app.route('/db/update/themes')
def updateThemes():
    animeList = Anime.query.all()
    for anime in animeList:
        themes = json.loads(anime.themes)
        themeIndex = 0
        for theme in themes:
            theme['extras'] = {'views': 0, 'likes': 0, 'dislikes': 0, 'malId': anime.malId}
            mirrorIndex = 0
            for mirror in theme.get('mirror'):
                mirror['appUrl'] = '{}/{}/{}'.format(anime.malId,
                                                     themeIndex,
                                                     mirrorIndex)
                mirrorIndex += 1
            themeIndex += 1
        anime.themes = json.dumps(themes)
    db.session.commit()


@app.route('/api/v1/top/<int:size>')
def get_most_viewed(size):
    queryList = Anime.query.all()
    themeList = []
    for anime in queryList:
        for theme in json.loads(anime.themes):
            # if not len(theme.get('title')):
            #    theme['title'] = theme['type']
            themeList.append(theme)
    # themeList = sorted(themeList, key=lambda k: k['title'], reverse=False)
    themeList = sorted(themeList, key=lambda k: k['extras']['views'], reverse=True)
    returnList = []
    i = 0

    while i < size:
        anime = Anime.query.filter_by(malId=themeList[i]['extras']['malId']).first()
        entry = {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
                 'year': anime.year, 'themes': [themeList[i]]}
        returnList.append(entry)
        i += 1
    return jsonify(returnList)


@app.route('/api/v1/themes/<string:name>')
def search_by_theme(name):
    animeList = Anime.query.all()
    themeList = []
    for anime in animeList:
        for theme in json.loads(anime.themes):
            if name.lower() in theme.get('title').lower():
                themeList.append(theme)
    searchList = []
    for theme in themeList:
        anime = Anime.query.filter_by(malId=theme.get('extras')['malId']).first()
        entry = {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
                 'year': anime.year, 'themes': [theme]}
        searchList.append(entry)
    return jsonify(searchList)


# LEGACY ROUTES

def getAnime(malId, poster=False, entry=None):
    anime = Anime.query.filter_by(malId=malId).first()
    if anime is not None:
        name = json.loads(anime.title)[0]
        alternate = json.loads(anime.title)
        malId = anime.malId
        themes = anime.themes
        year = anime.year
        season = anime.season
        poster = anime.cover
        return {'malId': malId, 'name': name, 'alternate': alternate, 'poster': poster, 'season': season,
                'themes': json.loads(themes)}
    return None


def getVideo(malId, themeType):
    anime = getAnime(malId)
    try:
        anime = anime['themes']
    except KeyError:
        return None
    themes = []
    for theme in anime:
        entry = {'title': theme['title'], 'type': theme['type']}
        themes.append(entry)
        if theme['type'].lower() == themeType.lower():
            return (theme.get('mirror')[0]['mirrorUrl'], theme['title'], theme['type'])
    return [{'message': 'theme not found'}, {'themes available': themes}]


def getAudio(url, title):
    videoFile = ['curl', url, '--output', './assets/video.webm']
    subprocess.run(videoFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    printable = set(string.printable)
    fileTitle = ''.join(filter(lambda x: x in printable, title[0]))
    animeTitle = ''.join(filter(lambda x: x in printable, title[1]))
    filename = './assets/{} - {} ({}).mp3'.format(fileTitle, animeTitle, title[2])
    ffmpeg = ['ffmpeg', '-i', './assets/video.webm', '-vn', '-c:a', 'libmp3lame', '-b:a', '320k',
              '-metadata', "title='" + title[0] + "'", filename, "-y"]
    subprocess.run(ffmpeg)
    response = fileioapi.upload(filename, "1w")
    subprocess.run(['rm', './assets/video.webm', filename])
    return response.get("link")


def getBodies(urlList):
    def load_url(url, timeout):
        return requests.get(url, timeout=timeout)

    bodies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(load_url, url, 30): url for url in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if len(data.content) > 2:
                bodies.append(data.content)
    return bodies


def getList(user):
    urlList = ['https://myanimelist.net/animelist/{}/load.json?offset={}&status=7'.format(user, i) for i in
               range(0, 300 * 4, 300)]
    bodies = getBodies(urlList)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    malList = []
    for data in content:
        for entry in json.loads(data):
            anime = getAnime(entry['anime_id'], False, entry)
            if anime is not None:
                malList.append(anime)
    malList = sorted(malList, key=lambda k: k['name'])
    return malList


def returnJson(obj):
    response = app.response_class(json.dumps(obj, sort_keys=False), mimetype=app.config['JSONIFY_MIMETYPE'])
    return response


@app.route('/u/<string:user>/')
def getAnimeList(user):
    malList = getList(user)
    return returnJson(malList)


@app.route('/id/<int:id>/<string:type>/')
def videoById(id, type):
    type = type.lower()
    anime = Anime.query.filter_by(malId=id).first()
    themes = json.loads(anime.themes)
    for theme in themes:
        if theme['type'].lower() == type:
            return redirect(theme['mirror'][0]['mirrorUrl'])
    return returnJson({'type not found': 'check /id/{}/ for available themes'.format(id)})


@app.route('/id/<int:id>/<string:type>/audio')
def audioById(id, type):
    type = type.lower()
    anime = Anime.query.filter_by(malId=id).first()
    themes = json.loads(anime.themes)
    for theme in themes:
        if theme['type'].lower() == type:
            title = [theme['title'], json.loads(anime.title)[0], theme['type']]
            url = theme['mirror'][0]['mirrorUrl']
            return redirect(getAudio(url, title))
    return returnJson({'type not found': 'check /id/{}/ for available themes'.format(id)})


@app.route('/id/<int:id>/')
def themesByID(id):
    anime = getAnime(id)
    if anime is None:
        return returnJson(
            {'message': "this anime isn't available in r/AnimeThemes. Send me a message if it is to u/LetrixZ"})
    # return returnJson({'malId': id, 'name':anime.name, 'themes':json.loads(anime.themes)})
    return returnJson(anime)


@app.route('/anime/<int:id>/')
def getAnimeThemes(id):
    return returnJson(getAnime(id))


@app.route('/')
def index():
    return returnJson({'message': 'animethemes api', 'author': 'u/LetrixZ', 'docs': '/apidoc'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
