import json

from models import object_decoder
from data.repo import anime_list, artist_list, theme_list


def get_latest_data(app=False):
    # a_list = json.load(open('src/data/anime_new.json', 'r', encoding="utf8"), object_hook=object_decoder)
    # ar_list = json.load(open('src/data/artist_new.json', 'r', encoding="utf8"), object_hook=object_decoder)
    # t_list = json.load(open('src/data/themes_new.json', 'r', encoding="utf8"), object_hook=object_decoder)
    if app:
        a_list = [item.app(False) for item in anime_list[-9:]]
        ar_list = [item.app() for item in artist_list[-6:]]
        t_list = [item.parse(True) for item in theme_list[-6:]]
        response = {'latest_anime': a_list, 'latest_artist': ar_list, 'latest_themes': t_list}
        return response
    else:
        a_list = [item.parse() for item in anime_list[-15:]]
        ar_list = [item.parse() for item in artist_list[-15:]]
        t_list = [item.parse() for item in theme_list[-10:]]
        return {'anime_list': a_list, 'artist_list': ar_list, 'theme_list': t_list}
