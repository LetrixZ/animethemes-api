import json
import random
import string

from flask import Flask, jsonify, request
from config import config
from models import db, Anime, User, Playlist
from anilist import getListFromUser
from flask_apidoc_extend import ApiDoc
from scrapers import addYear, getUserList, getAllYears, getAllSeasons, getYearSeasons, getCurrentSeason, getSeason, \
    getCoverFromDB


def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


enviroment = config['production']

app = create_app(enviroment)
ApiDoc(app=app)


def randomString(stringLength=8):
    letters = string.ascii_lowercase + "123456789" + string.ascii_lowercase.upper()
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_user(name, password):
    return User.create(name.lower(), password)


@app.route('/playlist/login', methods=['POST'])
def login():
    content = request.get_json()
    print(content)
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
    print(content)
    playlists = content.get('collection')
    playId = content.get('playId')
    actualPlaylist = content.get('actual_pos')
    row = Playlist.query.filter_by(playId=playId).first()
    if row:
        row.playlists = json.dumps(playlists)
        row.actualPlaylist = actualPlaylist
        row.update()
    return jsonify({'message': "{} saved succesfully".format(playId)})


# GET PLAYLIS COLLECTION
@app.route('/playlist/get', methods=['POST'])
def get_playlists():
    content = request.get_json()
    print(content)
    playId = content.get('message')
    row = Playlist.query.filter_by(playId=playId).first()
    playlist = row.json()
    print("response {}".format(playlist))
    return jsonify(playlist)


@app.route('/playlist/generate')
def create_playid():
    playId = randomString(6)
    while Playlist.query.filter_by(playId=playId).first() is not None:
        playId = randomString(6)
    Playlist.create(playId)
    return jsonify({'message': playId})


@app.route('/db/covers')
def get_all_covers():
    return jsonify(getCoverFromDB())


@app.route('/db/year/<string:year>')
def add_year_to_db(year):
    animeList = addYear(year)
    for anime in animeList[0]:
        Anime.create(json.dumps(anime['titles']), anime['malId'], anime['cover'], anime['year'], anime['season'],
                     json.dumps(anime['themes']))
    return jsonify(animeList[1])


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


@app.route('/api/v1/anime/<int:id>')
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
    return jsonify(
        {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
         'year': anime.year, 'themes': json.loads(anime.themes)})


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
    return jsonify(getSeason(year, current_season))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
