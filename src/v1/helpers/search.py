from models import *


def search_theme(name):
    # print(f'Searching theme {name}')
    results = Theme.query.filter(Theme.title.ilike("%{}%".format(name))).all()
    theme_list = []
    for theme in results:
        theme_list.append(theme.json())
    return theme_list

# Deprecated
# def search_anime(name):
#     results = Anime.query.all()
#     anime_list = []
#     for anime in results:
#         if name.lower() in str(anime.title).lower():
#             anime_list.append(anime.json())
#     return anime_list


def search_anime_2(name):
    # print(f'Searching anime {name}')
    results = Anime.query.filter(Anime.title.ilike(f'%{name}%'))
    results = results.limit(20)
    anime_list = []
    for anime in results:
        anime_list.append(anime.json())
    return anime_list


def search_artist(name):
    # print(f'Searching artist {name}')
    results = Artist.query.filter(Artist.name.ilike("%{}%".format(name))).all()
    artist_list = []
    for artist in results:
        artist_list.append(artist.json())
    return artist_list
