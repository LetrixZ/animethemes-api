import json

from src.models import object_decoder

anime_list = json.load(open('data/anime.json', 'r', encoding='utf8'), object_hook=object_decoder)
theme_list = json.load(open('data/themes.json', 'r', encoding='utf8'), object_hook=object_decoder)
artist_list = json.load(open('data/artist.json', 'r', encoding="utf8"), object_hook=object_decoder)
