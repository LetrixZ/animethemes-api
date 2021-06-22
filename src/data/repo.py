import json

<<<<<<< HEAD
from models import object_decoder
=======
from src.models import object_decoder
>>>>>>> b5795fde038c5903a2a7fed45b73855fe98d1588

anime_list = json.load(open('src/data/anime.json', 'r', encoding='utf8'), object_hook=object_decoder)
theme_list = json.load(open('src/data/themes.json', 'r', encoding='utf8'), object_hook=object_decoder)
artist_list = json.load(open('src/data/artist.json', 'r', encoding="utf8"), object_hook=object_decoder)