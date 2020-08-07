import concurrent
import json
import random
import string
import subprocess

import fileioapi as fileioapi
import requests
from anilist import getListFromUser
from artist_scraper import get_artists_list
from audio_scraper import get_music
from config import config
from flask import Flask, jsonify, request
from models import db, Anime, User, Playlist, Theme, Artist
from scrapers import getUserList, getAllYears, getAllSeasons, getYearSeasons, getSeason, \
    get_entry, get_artist_entry
from scrapersv2 import get_year as v2_get_year
from werkzeug.utils import redirect


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


def random_string(string_length=8):
    letters = string.ascii_lowercase + "123456789" + string.ascii_lowercase.upper()
    return ''.join(random.choice(letters) for i in range(string_length))


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


# GENERAL ROUTES

@app.route('/api/v1/anime/<int:mal_id>')
def get_anime(mal_id):
    anime = Anime.query.filter_by(malId=mal_id).first()
    if anime:
        return jsonify(get_entry(anime))
    else:
        return jsonify({'message': 'anime not found'})


@app.route('/api/v1/seasons/<string:year>/<string:season>')
def season(year, season):
    year = year.replace('s', '')
    return jsonify(getSeason(year, season))


@app.route('/api/v1/seasons/<string:year>')
def year_seasons(year):
    year = year.replace('s', '')
    return jsonify(getYearSeasons(year))


@app.route('/api/v1/years')
def get_years():
    return jsonify(getAllYears())


@app.route('/api/v1/seasons')
def get_seasons():
    return jsonify(getAllSeasons())


@app.route('/api/v1/year/<string:year>')
def get_year(year):
    year = int(str(year).replace('s', ''))
    results = Anime.query.filter_by(year=year).all()
    anime_list = []
    for anime in results:
        anime_list.append(get_entry(anime))
    return jsonify(anime_list)


@app.route('/u/<path:user>/')
@app.route('/api/v1/mal/<path:user>')
def get_mal_list(user):
    mal_list = getUserList(user)
    return jsonify(mal_list)


@app.route('/api/v1/anilist/<string:user>')
def get_anilist(user):
    ani_list = getListFromUser(user)
    anime_list = []
    for item in ani_list:
        mal_id = item['media']['idMal']
        anime = Anime.query.filter_by(malId=mal_id).first()
        if anime:
            anime_list.append(get_entry(anime))
            # themes = Theme.query.filter_by(mal_id=anime.malId).all()
            # theme_list = []
            # for theme in themes:
            #     theme_list.append(theme.json())
            # anime_list.append(
            #     {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover,
            #      'season': anime.season,
            #      'year': anime.year, 'themes': theme_list})
    anime_list = sorted(anime_list, key=lambda k: k['title'])
    return jsonify(anime_list)


@app.route('/api/v1/current/')
def current_season():
    seasons = ['Fall', 'Summer', 'Spring', 'Winter']
    year = Anime.query.order_by(Anime.year.desc()).first().year
    current = 'Winter'
    for i in range(4):
        if Anime.query.filter_by(season='{} {}'.format(seasons[i], year)).first():
            current = seasons[i]
            break
    anime_list = Anime.query.filter_by(season='{} {}'.format(current, year)).all()
    result_list = []
    for anime in anime_list:
        result_list.append(get_entry(anime))
    return jsonify(result_list)


@app.route('/api/v1/latest/themes/')
def latest_themes_added():
    theme_list = Theme.query.order_by(Theme.id.desc()).limit(15)
    result_list = []
    for theme in theme_list:
        anime = Anime.query.filter_by(malId=theme.mal_id).first()
        result_list.append(
            {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.json()]})
    return jsonify(result_list)


@app.route('/api/v1/latest/animes/')
def latest_animes_list():
    anime_list = Anime.query.order_by(Anime.id.desc()).limit(15)
    result_list = []
    for anime in anime_list:
        result_list.append(get_entry(anime))
    return jsonify(result_list)


@app.route('/api/v1/anime/<int:mal_id>/<string:theme_index>/<int:version>/video')
@app.route('/api/v1/anime/<int:mal_id>/<string:theme_index>/<int:version>')
def get_theme(mal_id, theme_index, version):
    anime = Anime.query.filter_by(malId=mal_id).first()
    if len(theme_index) == 1:
        theme_index = '0' + theme_index
    if anime:
        theme = Theme.query.filter_by(theme_id='{}-{}'.format(mal_id, theme_index)).first()
        if theme:
            theme.views += 1
            theme.update()
            try:
                return redirect(json.loads(theme.mirrors)[version].get('mirrorUrl'))
            except IndexError:
                return jsonify({'message': 'error bad index'})
        else:
            return jsonify({'message': 'bad index'})
    else:
        return jsonify({'message': 'anime not found'})


@app.route('/api/v1/anime/<int:mal_id>/<string:theme_index>/<int:version>/audio')
def get_audio_theme(mal_id, theme_index, version):
    anime = Anime.query.filter_by(malId=mal_id).first()
    if len(theme_index) == 1:
        theme_index = '0' + theme_index
    theme = Theme.query.filter_by(theme_id='{}-{}'.format(mal_id, theme_index)).first()
    if theme:
        title = [theme.title, json.loads(anime.title)[0], theme.type]
        url = theme.mirrors[version]
        return redirect(getAudio(url, title))
    else:
        return redirect("/anime/{}".format(id))


@app.route('/api/v1/top/')
def get_top():
    theme_list = Theme.query.order_by(Theme.views.desc()).limit(15)
    result_list = []
    for theme in theme_list:
        anime = Anime.query.filter_by(malId=theme.mal_id).first()
        result_list.append(
            {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.json()]})
    return jsonify(result_list)


@app.route('/api/v1/s/theme/<path:name>')
def search_theme(name):
    results = Theme.query.filter(Theme.title.ilike("%{}%".format(name))).all()
    search_list = []
    for item in results:
        search_list.append(item.single_json())
    return jsonify(search_list)


@app.route('/api/v1/s/anime/<path:name>')
@app.route('/api/v1/s/<path:name>')
def search_anime(name):
    results = Anime.query.filter(Anime.title.ilike("%{}%".format(name))).all()
    animeList = []
    for item in results:
        animeList.append(get_entry(item))
    return jsonify(animeList)


@app.route('/api/v1/s/artist/<path:name>')
def search_artist(name):
    results = Artist.query.filter(Artist.name.ilike("%{}%".format(name))).all()
    artist_list = []
    for item in results:
        # artist_list.append(get_artist_entry(item))
        artist_list.append(item.json())
    return jsonify(artist_list)


@app.route('/api/v1/s/all/<path:name>')
def search_all(name):
    theme_query = Theme.query.filter(Theme.title.ilike("%{}%".format(name))).all()
    theme_list = []
    for theme in theme_query:
        theme_list.append(theme.single_json())

    anime_query = Anime.query.filter(Anime.title.ilike("%{}%".format(name))).all()
    anime_list = []
    for anime in anime_query:
        anime_list.append(get_entry(anime))

    artist_query = Artist.query.filter(Artist.name.ilike("%{}%".format(name))).all()
    artist_list = []
    for artist in artist_query:
        artist_list.append(artist.json())

    return jsonify({'anime_list': {'animeList': anime_list, 'title': 'Anime', 'type': 0},
                    'theme_list': {'animeList': theme_list, 'title': 'Theme', 'type': 1},
                    'artist_list': artist_list})


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


def getAnimeList(user):
    malList = getList(user)
    return returnJson(malList)


@app.route('/api/v1/anime/<int:id>/<string:type>/')
@app.route('/api/v1/id/<int:id>/<string:type>/')
@app.route('/id/<int:id>/<string:type>/')
def video_by_id(id, type):
    type = type.lower()
    anime = Anime.query.filter_by(malId=id).first()
    # themes = json.loads(anime.themes)
    themes = Theme.query.filter_by(mal_id=id).all()
    for theme in themes:
        if theme.type.lower() == type:
            return redirect(json.loads(theme.mirrors)[0]['mirrorUrl'])
    # return returnJson({'type not found': 'check /id/{}/ for available themes'.format(id)})
    return redirect("/id/{}".format(id))


@app.route('/api/v1/anime/<int:id>/<string:type>/audio')
@app.route('/api/v1/id/<int:id>/<string:type>/audio')
@app.route('/id/<int:id>/<string:type>/audio')
def audio_by_id(id, type):
    type = type.lower()
    anime = Anime.query.filter_by(malId=id).first()
    themes = Theme.query.filter_by(mal_id=id).all()
    for theme in themes:
        if theme.type.lower() == type:
            title = [theme.title, json.loads(anime.title)[0], theme.type]
            url = json.loads(theme.mirrors)[0]['mirrorUrl']
            return redirect(getAudio(url, title))
    # return returnJson({'type not found': 'check /id/{}/ for available themes'.format(id)})
    return redirect("/id/{}".format(id))


@app.route('/anime/<int:id>/')
@app.route('/id/<int:id>/')
def themes_by_id(id):
    # anime = getAnime(id)
    entry = Anime.query.filter_by(malId=id).first()
    if entry is None:
        return returnJson(
            {'message': "this anime isn't available in r/AnimeThemes. Send me a message if it is to u/LetrixZ"})
    anime = get_entry(entry)
    return returnJson(anime)


# APP ROUTES
@app.route('/app_list/')
def get_app_list():
    # Latest themes list
    theme_list = Theme.query.order_by(Theme.id.desc()).limit(15)
    latest_themes_list = []
    for theme in theme_list:
        anime = Anime.query.filter_by(malId=theme.mal_id).first()
        latest_themes_list.append(
            {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.json()]})

    # Latest anime list
    anime_list = Anime.query.order_by(Anime.id.desc()).limit(15)
    latest_anime_added = []
    for anime in anime_list:
        latest_anime_added.append(get_entry(anime))

    # Top list
    theme_list = Theme.query.order_by(Theme.views.desc()).limit(15)
    top_list = []
    for theme in theme_list:
        anime = Anime.query.filter_by(malId=theme.mal_id).first()
        top_list.append(
            {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.json()]})

    # Current Season
    seasons = ['Fall', 'Summer', 'Spring', 'Winter']
    year = Anime.query.order_by(Anime.year.desc()).first().year
    current = 'Winter'
    for i in range(4):
        if Anime.query.filter_by(season='{} {}'.format(seasons[i], year)).first():
            current = seasons[i]
            break
    anime_list = Anime.query.filter_by(season='{} {}'.format(current, year)).all()
    current_list = []
    for anime in anime_list:
        current_list.append(get_entry(anime))

    return jsonify({'yearList': getAllSeasons(),
                    'animeLists': [{'animeList': current_list, 'title': "{} {}".format(current, year), 'type': 2},
                                   {'animeList': top_list,
                                    'title': 'Top 15 themes', 'type': 3},
                                   {'animeList': latest_anime_added,
                                    'title': 'Latest animes added', 'type': 5},
                                   {'animeList': latest_themes_list,
                                    'title': 'Latest themes added', 'type': 4}]})


@app.route('/app/count/<int:mal_id>/<string:theme_index>')
def count_view(mal_id, theme_index):
    if len(theme_index) == 1:
        theme_index = '0' + theme_index
    print("{}, {}".format(mal_id, theme_index))
    anime = Anime.query.filter_by(malId=mal_id).first()
    if anime:
        theme = Theme.query.filter_by(theme_id='{}-{}'.format(mal_id, theme_index)).first()
        if theme:
            theme.views += 1
            theme.update()
            try:
                return jsonify(theme.views)
            except IndexError:
                return jsonify({'message': 'error bad index'})
        else:
            return jsonify({'message': 'bad index'})
    else:
        return jsonify({'message': 'anime not found'})


@app.route('/app/update_pinned', methods=['POST'])
def update_pinned():
    content = request.get_json()
    anime_list = content.get('animeList')
    result_list = []
    for anime in anime_list:
        anime_entry = Anime.query.filter_by(malId=anime.get('malId')).first()
        result_list.append(get_entry(anime_entry))
    return jsonify({'animeList': result_list, 'title': 'Pinned', 'type': 0})


# DB ROUTES

@app.route('/db/get_artists')
def get_artists():
    return jsonify(get_artists_list())


@app.route('/db/list_covers')
def list_faulty_covers():
    anime_list = Anime.query.filter(Anime.cover.ilike("%?s=%")).all()
    return_list = []
    for item in anime_list:
        item.cover = item.cover[:item.cover.find(".jpg") + 4]
        return_list.append(item.json())
    db.session.commit()
    return jsonify(return_list)


@app.route('/db/update_themes')
def update_themes():
    theme_list = Theme.query.all()
    for theme in theme_list:
        mal_id = theme.mal_id
        index = theme.theme_id.split('-')[1]
        if len(index) == 1:
            index = "0" + index
        theme.theme_id = str(mal_id) + '-' + index
        # theme.save()
    db.session.commit()


@app.route('/db/add_themes/')
def add_themes_db():
    animeList = Anime.query.all()
    themeList = []
    for anime in animeList:
        index = 0
        for theme in json.loads(anime.themes):
            entry = Theme.create(theme.get('title'), theme.get('type'), anime.malId,
                                 '{}/{}'.format(anime.malId, index), theme.get('notes'),
                                 json.dumps(theme.get('mirror')))
            if entry:
                themeList.append(entry)
            index += 1
    print('finished')
    db.session.add_all(themeList)
    print('all added {}'.format(len(themeList)))
    db.session.commit()
    print('commited')
    return jsonify(themeList)


@app.route('/db/year/<string:year>')
def add_year(year):
    anime_list = v2_get_year(year)
    for season_list in anime_list:
        for anime in season_list:
            Anime.create(json.dumps(anime['titles']), anime['malId'], anime['cover'], anime['year'], anime['season'],
                         json.dumps(anime['themes']))
    return jsonify(anime_list)


@app.route('/db/print_all/')
def print_all():
    anime_list = Anime.query.all()
    print_list = []
    for anime in anime_list:
        print_list.append(anime.json())
    return jsonify(print_list)


@app.route('/db/music/')
def db_add_music():
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


@app.route('/db/music/mirror/')
def db_add_music_mirror():
    anime_list = Anime.query.all()
    for anime in anime_list:
        anime_title = json.loads(anime.title)[0]
        anime_title = anime_title.replace(":", "")
        if len(anime_title) >= 3:
            themes = json.loads(anime.themes)
            for theme in themes:
                if not theme.get('audio').get('mirror'):
                    item = get_music(anime)
                    anime.themes = json.dumps(item)
                    db.session.commit()
                    break
    return jsonify({'message': 'done'})


@app.route('/db/nomusic/')
def no_music():
    anime_list = Anime.query.all()
    theme_list = []
    for anime in anime_list:
        themes = json.loads(anime.themes)
        for theme in themes:
            if theme.get('audio').get('mirror') is None:
                theme_list.append(
                    {'anime': json.loads(anime.title), 'mal_id': anime.malId, 'theme_title': theme.get('title')})
    return jsonify(theme_list)


@app.route('/db/addmusic/<int:malId>/<string:name>')
def get_music_web(malId, name):
    anime = Anime.query.filter_by(malId=malId).first()
    themes = json.loads(anime.themes)
    added = []
    for theme in themes:
        if not theme.get('audio').get('mirror'):
            item = get_music(anime, name)
            added.append({'anime': json.loads(anime.title), 'mal_id': anime.malId, 'theme_list': item})
            anime.themes = json.dumps(item)
            db.session.commit()
            break
    return jsonify(added)


@app.route('/')
def index():
    return returnJson(
        {'message': 'animethemes api', 'author': 'u/LetrixZ', 'docs': 'https://github.com/LetrixZ/animethemes-api'})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
