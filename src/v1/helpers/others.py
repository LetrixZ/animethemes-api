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
        result_list.append(theme.json_info_extended())
    return result_list


def top_themes(limit):
    theme_list = Theme.query.order_by(Theme.views.desc()).limit(limit)
    result_list = []
    for theme in theme_list:
        result_list.append(theme.json_info_extended())
    return result_list
