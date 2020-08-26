import requests, json

from models import Anime, Artist


def get_anime_covers():
    anime_list = json.loads(requests.get('http://animethemes-api.herokuapp.com/db/print_all').content)
    for item in anime_list:
        anime = Anime.query.filter_by(mal_id=item['malId']).first()
        anime.cover = item['cover']
        anime.save()
    return {'message': 'done'}


def get_artists():
    artist_list = json.loads(requests.get('http://animethemes-api.herokuapp.com/db/print_all_artist').content)
    for item in artist_list:
        Artist.create(name=item['name'], mal_id=item['mal_id'], cover=item['cover'], themes=item['themes'])
