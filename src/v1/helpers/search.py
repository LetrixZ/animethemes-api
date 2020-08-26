from sqlalchemy import text, String, func

from models import Artist, Anime, Theme, db


def search_theme(name):
    results = Theme.query.filter(Theme.title.ilike("%{}%".format(name))).all()
    theme_list = []
    for theme in results:
        theme_list.append(theme.json())
    return theme_list


def search_anime(name):
    results = Anime.query.all()
    anime_list = []
    for anime in results:
        if name.lower() in str(anime.title).lower():
            anime_list.append(anime.json())
    return anime_list


def search_artist(name):
    results = Artist.query.filter(Artist.name.ilike("%{}%".format(name))).all()
    artist_list = []
    for artist in results:
        artist_list.append(artist.json())
    return artist_list
