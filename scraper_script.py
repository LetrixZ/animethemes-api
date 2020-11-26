import dataclasses
import json

from scrapers.anime_themes_scraper import get_year, get_cover
from scrapers.artist_scraper import get_list

anime_list = json.load(open('data/anime.json', 'r', encoding="utf8"))
theme_list = json.load(open('data/themes.json', 'r', encoding="utf8"))
artist_list = json.load(open('data/artist.json', 'r', encoding='utf8'))
cover_list = json.load(open('data/covers.json', 'r', encoding='utf8'))


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def get_all_years():
    years = ['60s', '70s', '80s', '90s', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
             '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    a_list = []
    t_list = []
    for year in years:
        year_list = get_year(year)
        a_list += year_list[0]
        t_list += year_list[1]
        print(len(t_list))
        print(len(a_list))
    with open('data/anime.json', 'w') as f:
        json.dump(a_list, f, cls=EnhancedJSONEncoder)
    with open('data/themes.json', 'w') as f:
        json.dump(t_list, f, cls=EnhancedJSONEncoder)


def get_artists(theme_list_db):
    artist_list = get_list(theme_list_db)
    with open('data/artist.json', 'w') as f:
        json.dump(artist_list, f, cls=EnhancedJSONEncoder)


def add_covers():
    for anime in anime_list:
        cover = [item['cover'] for item in cover_list if anime['anime_id'] == item['mal_id']]
        if cover:
            anime['cover'] = cover
        else:
            print(anime)
            cover = get_cover(anime['anime_id'])
            anime['cover'] = cover
            cover_list.append({'mal_id': anime['anime_id'], 'cover': cover})
    with open('data/anime.json', 'w') as f:
        json.dump(anime_list, f, cls=EnhancedJSONEncoder)
    for artist in artist_list:
        cover = [item['cover'] for item in cover_list if artist['artist_id'] == item['mal_id']]
        if cover:
            artist['cover'] = cover
        else:
            print(artist)
            cover = get_cover(artist['artist_id'])
            artist['cover'] = cover
            cover_list.append({'mal_id': artist['artist_id'], 'cover': cover})
    with open('data/artist.json', 'w') as f:
        json.dump(artist_list, f, cls=EnhancedJSONEncoder)
    with open('data/covers.json', 'w') as f:
        json.dump(cover_list, f, cls=EnhancedJSONEncoder)


def assign_artists():
    for artist in artist_list:
        for theme_id in artist['themes']:
            entry = next((item for item in theme_list if item["theme_id"] == theme_id), None)
            if entry:
                entry['artist_id'] = artist['artist_id']
    with open('data/themes.json', 'w') as f:
        json.dump(theme_list, f, cls=EnhancedJSONEncoder)
    return 'Artist assigment successfull'


# get_all_years()
# get_artists(theme_list)
assign_artists()
add_covers()
