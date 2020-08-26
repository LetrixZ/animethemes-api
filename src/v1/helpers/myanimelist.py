import concurrent.futures
import json

import requests

from models import Anime

filters = {'all': 7, 'watching': 1, 'completed': 2, 'hold': 3, 'dropped': 4, 'planning': 6}


def get_bodies(url_list):
    # ASYNC REQUEST?
    def load_url(url, timeout):
        return requests.get(url, timeout=timeout)

    bodies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(load_url, url, 30): url for url in url_list}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if len(data.content) > 10:
                bodies.append(data.content)
    return bodies


def get_mal_list(user, list_filter):
    # LIST REQUEST
    url_list = [f'https://myanimelist.net/animelist/{user}/load.json?offset={i}&status={list_filter}'
                for i in range(0, 300 * 10, 300)]
    print(url_list)
    bodies = get_bodies(url_list)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    mal_list = []
    # FILTERING
    for page in content:
        for entry in json.loads(page):
            anime = Anime.query.filter_by(mal_id=entry['anime_id']).first()
            if anime:
                mal_list.append(anime.json())
    mal_list = sorted(mal_list, key=lambda k: k['title'])
    return mal_list
