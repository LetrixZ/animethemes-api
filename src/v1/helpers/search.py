from difflib import SequenceMatcher

from models import Artist, Anime


def search_theme(name):
    anime_list = Anime.query.all()
    theme_list = []
    for anime in anime_list:
        for theme in anime.themes:
            if SequenceMatcher(a=theme['title'].lower(), b=name.lower()).ratio() > 0.8:
                theme_list.append(theme)
            elif name.lower() in theme['title'].lower() and theme['title'] != "":
                theme_list.append(theme)
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
