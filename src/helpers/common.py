import json

from src.models import object_decoder


def get_latest_data(app=False):
    a_list = json.load(open('src/data/anime_new.json', 'r', encoding="utf8"), object_hook=object_decoder)
    ar_list = json.load(open('src/data/artist_new.json', 'r', encoding="utf8"), object_hook=object_decoder)
    t_list = json.load(open('src/data/themes_new.json', 'r', encoding="utf8"), object_hook=object_decoder)
    if app:
        anime_list = [item.app(False) for item in a_list]
        artist_list = [item.app() for item in ar_list]
        theme_list = [item.parse(True) for item in t_list]
        response = {}
        if len(a_list) > 0:
            response['latest_anime'] = anime_list
        if len(ar_list) > 0:
            response['latest_artist'] = artist_list
        if len(t_list) > 0:
            response['latest_themes'] = theme_list
        return response
    else:
        anime_list = [item.parse() for item in a_list]
        artist_list = [item.parse() for item in ar_list]
        theme_list = [item.parse() for item in t_list]
        return {'anime_list': anime_list, 'artist_list': artist_list, 'theme_list': theme_list}
