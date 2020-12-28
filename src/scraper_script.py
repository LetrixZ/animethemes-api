import dataclasses
import json

from src.models import object_decoder
from src.scrapers.anime_themes_scraper import get_year, get_cover
from src.scrapers.artist_scraper import get_list, get_cover as get_cover_artist


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def get_all_years():
    print("get_all_years")
    years = ['60s', '70s', '80s', '90s', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
             '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    a_list = []
    t_list = []
    for year in years:
        year_list = get_year(year)
        a_list += year_list[0]
        t_list += year_list[1]
    with open('src/data/anime_new.json', 'w') as f:
        json.dump(a_list, f, cls=EnhancedJSONEncoder)
    with open('src/data/themes_new.json', 'w') as f:
        json.dump(t_list, f, cls=EnhancedJSONEncoder)


def get_artists(theme_list_db):
    print("get_artists")
    a_list = get_list(theme_list_db)
    with open('src/data/artist_new.json', 'w') as f:
        json.dump(a_list, f, cls=EnhancedJSONEncoder)


corrected_covers = {41911: 'https://cdn.myanimelist.net/images/anime/1984/110105.jpg',
                    40148: 'https://cdn.myanimelist.net/images/anime/1485/108385.jpg'}


def add_covers():
    print("add_covers")
    for anime in anime_list:
        cover = next((item['cover'] for item in cover_list if
                      anime.anime_id == item['mal_id'] and 'voiceactor' not in item['cover']), None)
        if cover:
            anime.cover = cover
        else:
            print(anime)
            cover = get_cover(anime.anime_id)
            anime.cover = cover
            cover_list.append({'mal_id': anime.anime_id, 'cover': cover})
    with open('src/data/anime.json', 'w') as f:
        json.dump(anime_list, f, cls=EnhancedJSONEncoder)
    for artist in artist_list:
        cover = next((item['cover'] for item in cover_list if
                      artist.artist_id == item['mal_id'] and 'voiceactor' in item['cover']), None)
        if cover:
            artist.cover = cover
        else:
            print(artist)
            cover = get_cover_artist(artist.artist_id)
            artist.cover = cover
            cover_list.append({'mal_id': artist.artist_id, 'cover': cover})
    with open('src/data/artist.json', 'w') as f:
        json.dump(artist_list, f, cls=EnhancedJSONEncoder)
    with open('src/data/covers.json', 'w') as f:
        json.dump(cover_list, f, cls=EnhancedJSONEncoder)

    new_anime = json.load(open('src/data/anime_new.json', 'r', encoding='utf8'), object_hook=object_decoder)
    new_artist = json.load(open('src/data/artist_new.json', 'r', encoding='utf8'), object_hook=object_decoder)

    for anime in new_anime:
        cover = next((item['cover'] for item in cover_list if
                      anime.anime_id == item['mal_id'] and 'voiceactor' not in item['cover']), None)
        if cover:
            anime.cover = cover
        else:
            print(anime)
            cover = get_cover(anime.anime_id)
            anime.cover = cover
            cover_list.append({'mal_id': anime.anime_id, 'cover': cover})
    with open('src/data/anime_new.json', 'w') as f:
        json.dump(new_anime, f, cls=EnhancedJSONEncoder)
    for artist in new_artist:
        cover = next((item['cover'] for item in cover_list if
                      artist.artist_id == item['mal_id'] and 'voiceactor' in item['cover']), None)
        if cover:
            artist.cover = cover
        else:
            print(artist)
            cover = get_cover_artist(artist.artist_id)
            artist.cover = cover
            cover_list.append({'mal_id': artist.artist_id, 'cover': cover})
    with open('src/data/artist_new.json', 'w') as f:
        json.dump(new_artist, f, cls=EnhancedJSONEncoder)


def assign_artists():
    print("assing_artists")
    for artist in artist_list:
        for theme_id in artist.themes:
            entry = next((item for item in theme_list if item.theme_id == theme_id), None)
            if entry:
                entry.artist_id = artist.artist_id
    with open('src/data/themes.json', 'w') as f:
        json.dump(theme_list, f, cls=EnhancedJSONEncoder)
    return 'Artist assigment successfull'


def update_data():
    print("update_data")
    new_anime = json.load(open('src/data/anime_new.json', 'r', encoding='utf8'), object_hook=object_decoder)
    new_themes = json.load(open('src/data/themes_new.json', 'r', encoding='utf8'), object_hook=object_decoder)
    new_artist = json.load(open('src/data/artist_new.json', 'r', encoding='utf8'), object_hook=object_decoder)

    if len(new_anime) > 0:
        print("Adding anime")
        for anime in new_anime:
            anime_list.append(anime)
        with open('src/data/anime.json', 'w') as f:
            json.dump(anime_list, f, cls=EnhancedJSONEncoder)

    if len(new_themes) > 0:
        print("Adding themes")
        for theme in new_themes:
            theme_list.append(theme)
        with open('src/data/themes.json', 'w') as f:
            json.dump(theme_list, f, cls=EnhancedJSONEncoder)

    if len(new_artist) > 0:
        print("Adding artist")
        for artist in new_artist:
            artist_list.append(artist)
        with open('src/data/artist.json', 'w') as f:
            json.dump(artist_list, f, cls=EnhancedJSONEncoder)


anime_list = json.load(open('src/data/anime.json', 'r', encoding="utf8"), object_hook=object_decoder)
theme_list = json.load(open('src/data/themes.json', 'r', encoding="utf8"), object_hook=object_decoder)
artist_list = json.load(open('src/data/artist.json', 'r', encoding='utf8'), object_hook=object_decoder)
cover_list = json.load(open('src/data/covers.json', 'r', encoding='utf8'))

get_all_years()
get_artists(theme_list)
assign_artists()
update_data()
add_covers()
