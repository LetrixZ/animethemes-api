import json

import requests

BASE_URL = "https://api.jikan.moe/v3"


def get_anime_picture(anime_id):
    request = requests.get(f'{BASE_URL}/anime/{anime_id}/pictures')
    response = json.loads(request.content)
    return response['pictures'][0]['large']


def get_artist_picture(artist_id):
    request = requests.get(f'{BASE_URL}/person/{artist_id}/pictures')
    response = json.loads(request.content)
    return response['pictures'][0]['large']
