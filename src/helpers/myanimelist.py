import concurrent.futures
import json

import requests

<<<<<<< HEAD
from data.repo import anime_list
=======
from src.data.repo import anime_list
>>>>>>> b5795fde038c5903a2a7fed45b73855fe98d1588

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


def get_mal_list(user, list_filter, app=False):
    # LIST REQUEST
    url_list = [f'https://myanimelist.net/animelist/{user}/load.json?offset={i}&status={list_filter}'
                for i in range(0, 300 * 10, 300)]
    bodies = get_bodies(url_list)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    mal_list = []
    # FILTERING
    for page in content:
        for entry in json.loads(page):
            if entry == 'errors':
                return {'error': 'user not found'}
            if app:
                anime = next((item.app() for item in anime_list if item.anime_id == entry['anime_id']), None)
            else:
                anime = next((item.parse() for item in anime_list if item.anime_id == entry['anime_id']), None)
            if anime:
                mal_list.append(anime)
    mal_list = sorted(mal_list, key=lambda k: k['title'])
    return mal_list
