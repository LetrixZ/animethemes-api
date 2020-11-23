from models import Anime, Theme, Artist


def latest_anime(limit):
    anime_list = Anime.query.order_by(Anime.id.desc()).limit(limit)
    result_list = []
    for anime in anime_list:
        result_list.append(anime.json())
    return result_list


def latest_artist(limit):
    artist_list = Artist.query.order_by(Artist.id.desc()).limit(limit)
    result_list = []
    for artist in artist_list:
        result_list.append(artist.json())
    return result_list


def latest_themes(limit):
    theme_list = Theme.query.order_by(Theme.id.desc()).limit(limit)
    result_list = []
    for theme in theme_list:
        result_list.append(theme.json())
    return result_list


def top_themes(limit):
    theme_list = Theme.query.order_by(Theme.views.desc()).limit(limit)
    result_list = []
    for theme in theme_list:
        result_list.append(theme.json())
    return result_list


def all_anime():
    anime_list = Anime.query.all()
    result_list = []
    for anime in anime_list:
        result_list.append(anime.json_raw())
    return result_list


def all_theme():
    theme_list = Theme.query.all()
    result_list = []
    for theme in theme_list:
        result_list.append(theme.json())
    return result_list


def all_anime_page(page=1):
    query = Anime.query
    offset = 15 * (page - 1)
    query = query.limit(15)
    query = query.offset(offset)
    anime_list = []
    for anime in query:
        anime_list.append(anime.json())
    return anime_list


def all_themes_page(page=1):
    query = Theme.query
    offset = 15 * (page - 1)
    query = query.limit(15)
    query = query.offset(offset)
    theme_list = []
    for theme in query:
        theme_list.append(theme.json())
    return theme_list
