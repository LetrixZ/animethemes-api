import random
from flask import Blueprint, jsonify, url_for
from werkzeug.utils import redirect

from src.data.repo import anime_list, artist_list, theme_list
from src.helpers.common import get_latest_data
from src.routes.seasons import list_years, list_current_season

android = Blueprint('android', __name__)


@android.route("content")
def content():
    return jsonify(list_current_season(True))


@android.route('years')
def get_year_list():
    return jsonify(list_years(True))


@android.route('latest')
def get_latest():
    return jsonify(get_latest_data(True))


@android.route('home')
def get_home_list():
    home = {'year_list': list_years(True),
            'current_season': list_current_season(True)}
    home.update(get_latest_data(True))
    return jsonify(home)


@android.route('updates')
def get_updates():
    return jsonify(
        {'title': 'New version available!', 'message': 'This is a changelog', 'version': '1.0',
         'id': 1000})


@android.route('random')
def get_random_anime():
    return jsonify([item.app() for item in random.sample(anime_list, 15)])


@android.route('anime/<int:anime_id>')
def get_anime(anime_id):
    #if anime_id == 40060:
        # return '{"mal_id":40060,"title":"BNA","cover":"https://cdn.myanimelist.net/images/anime/1139/106986.jpg","year":2020,"season":"Spring 2020","themes":[{"title":"Ready to","theme_id":"40060-00","type":"OP V1","artist":null,"mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/BrandNewAnimal-OP1.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/40060-00/0/audio"}],"notes":"","episodes":"1-5","category":""},{"title":"Ready to","theme_id":"40060-01","type":"OP V2","artist":null,"mirrors":[{"quality":"","mirror":"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/40060-01/0/audio"}],"notes":"","episodes":"6-11","category":""},{"title":"NIGHT RUNNING","theme_id":"40060-02","type":"ED V1","artist":null,"mirrors":[{"quality":"","mirror":"https://animethemes.moe/video/BrandNewAnimal-ED1.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/40060-02/0/audio"}],"notes":"","episodes":"1-6","category":""},{"title":"NIGHT RUNNING","theme_id":"40060-03","type":"ED V2","artist":null,"mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/BrandNewAnimal-ED1v2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/40060-03/0/audio"}],"notes":"","episodes":"7-10","category":""},{"title":"NIGHT RUNNING","theme_id":"40060-04","type":"ED V3","artist":null,"mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/BrandNewAnimal-ED1v3.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/40060-04/0/audio"}],"notes":"","episodes":"11","category":""}]}'
    # if anime_id == 35062:
    #     return '{"mal_id":35062,"title":"Mahoutsukai no Yome","cover":"https://cdn.myanimelist.net/images/anime/3/88476.jpg","year":2017,"season":"Fall 2017","themes":[{"title":"Here","theme_id":"35062-00","type":"OP1","artist":"JUNNA","mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP1.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-00/0/audio"},{"quality":"Lyrics","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP1-Lyrics.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-00/1/audio"},{"quality":"NC, BD, 1080","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP1-NCBD1080.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-00/2/audio"}],"notes":null,"episodes":"1-12","category":null},{"title":"You","theme_id":"35062-01","type":"OP2 V1","artist":"Mayn","mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-01/0/audio"},{"quality":"NC, BD, 1080","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP2-NCBD1080.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-01/1/audio"}],"notes":null,"episodes":"13-23","category":null},{"title":"You","theme_id":"35062-02","type":"OP2 V2","artist":"Mayn","mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP2v2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-02/0/audio"},{"quality":"NC, BD, 1080","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-OP2v2-NCBD1080.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-02/1/audio"}],"notes":null,"episodes":"24","category":null},{"title":"Wa -cycle-","theme_id":"35062-03","type":"ED1","artist":null,"mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-ED1.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-03/0/audio"},{"quality":"Lyrics","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-ED1-Lyrics.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-03/1/audio"},{"quality":"NC, BD, 1080","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-ED1-NCBD1080.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-03/2/audio"}],"notes":null,"episodes":"1-12","category":null},{"title":"Tsuki no mou Hanbun","theme_id":"35062-04","type":"ED2","artist":null,"mirrors":[{"quality":"","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-ED2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-04/0/audio"},{"quality":"NC, BD, 1080","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-ED2-NCBD1080.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-04/1/audio"}],"notes":null,"episodes":"13-23","category":null},{"title":"The Legend of The Ancient Magus Bride","theme_id":"35062-05","type":"ED3","artist":null,"mirrors":[{"quality":"Trans, Subbed","mirror":"http://192.168.1.40/video/MahoutsukaiNoYome-ED3.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/35062-05/0/audio"}],"notes":"Spoiler","episodes":"24","category":null}]}'
    # if anime_id == 19815:
    #     return '{"mal_id":19815,"title":"No Game No Life","cover":"https://cdn.myanimelist.net/images/anime/5/65187.jpg","year":2014,"season":"Spring 2014","themes":[{"title":"This game","theme_id":"19815-00","type":"OP1","artist":"Konomi Suzuki","mirrors":[{"quality":"NC, BD, 1080","mirror":"http:/192.168.1.40/video/NoGameNoLife-OP1.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/19815-00/0/audio"}],"notes":null,"episodes":"1-8, 10, 12","category":null},{"title":"Onegai☆Snyaiper","theme_id":"19815-01","type":"OP2","artist":"Miyuki Sawashiro","mirrors":[{"quality":"BD, 1080, Subbed","mirror":"http:/192.168.1.40/video/NoGameNoLife-OP2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/19815-01/0/audio"}],"notes":null,"episodes":"11","category":null},{"title":"Oracion","theme_id":"19815-02","type":"ED V1","artist":"Ai Kayano","mirrors":[{"quality":"NC, BD, 1080","mirror":"http:/192.168.1.40/video/NoGameNoLife-ED1.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/19815-02/0/audio"}],"notes":null,"episodes":"2-7, 9-11","category":null},{"title":"Oracion","theme_id":"19815-03","type":"ED V2","artist":"Ai Kayano","mirrors":[{"quality":"BD, 1080","mirror":"http:/192.168.1.40/video/NoGameNoLife-ED1v2.webm","audio":"http://animethemes-api.herokuapp.com/api/v1/theme/19815-03/0/audio"}],"notes":"Spoiler","episodes":"8","category":null}]}'
    anime = next((item.app(True) for item in anime_list if item.anime_id == anime_id), None)
    return jsonify(anime)


@android.route('artist/<int:artist_id>')
def get_artist(artist_id):
    artist = next((item.parse() for item in artist_list if item.artist_id == artist_id), None)
    return jsonify(artist)


@android.route('theme/<string:theme_id>')
def get_theme(theme_id):
    theme = next((item.parse() for item in theme_list if item.theme_id == theme_id), None)
    return jsonify(theme)


@android.route('search/<path:name>')
def search_term(name):
    return jsonify({'anime_list': [item.app() for item in anime_list if name.lower() in item.title.lower()],
                    'theme_list': [item.parse(extended=True) for item in theme_list if
                                   name.lower() in item.title.lower()],
                    'artist_list': [item.app() for item in artist_list if name.lower() in item.name.lower()]})


@android.route('year/<int:year>')
def get_year(year):
    return redirect(url_for('season.list_year_season', year=year, app=True))


@android.route('mal/<string:user>')
def get_mal(user):
    return redirect(url_for('mal_list', user=user, app_r=True))


@android.route('anilist/<string:user>')
def get_anilist(user):
    return redirect(url_for('anilist_list', app_r=True, user=user))
