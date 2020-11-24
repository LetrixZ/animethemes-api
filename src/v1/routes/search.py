import json
import os

from flask import Blueprint, jsonify
import redis

from v1.helpers.search import *

search = Blueprint('search', __name__)
redis_instance = redis.from_url(os.getenv('REDIS_URL'))


@search.route('<path:name>')
def search_all_2(name):
    cached = redis_instance.get(f'search/{name}')
    data = {}
    if not cached:
        # print('Not cached')
        data = {'anime_list': search_anime_2(name),
                'theme_list': search_theme(name),
                'artist_list': search_artist(name)}
        redis_instance.setex(f'search/{name}', 24 * 60 * 60, json.dumps(data))
    else:
        # print('Cached')
        data = json.loads(redis_instance.get(f'search/{name}'))
    return jsonify(data)
