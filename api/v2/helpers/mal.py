import concurrent
import json

import requests

from api.models import Anime


def get_bodies(urlList):
    def load_url(url, timeout):
        return requests.get(url, timeout=timeout)

    bodies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(
            load_url, url, 30): url for url in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if len(data.content) > 2:
                bodies.append(data.content)
    return bodies


def get_user_list(user):
    url_list = ['https://myanimelist.net/animelist/{}/load.json?offset={}&status=7'.format(user, i) for i in
                range(0, 300 * 10, 300)]
    bodies = get_bodies(url_list)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    mal_list = []
    for page in content:
        for entry in json.loads(page):
            anime = Anime.objects.filter(mal_id=entry['anime_id']).first()
            if anime:
                mal_list.append(anime.json())
    mal_list = sorted(mal_list, key=lambda k: k['title'])
    return mal_list
