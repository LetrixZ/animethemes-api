from operator import itemgetter

import concurrent.futures
import json
import os
import praw
import requests

from src.models import Anime, Theme

client_secret = os.getenv('CLIENT_SECRET')

reddit = praw.Reddit(client_id="mS1uQkjEv2vxhg",
                     client_secret=client_secret,
                     user_agent="Letrix's AnimeThemes API")


def get_bodies(urlList):
    def load_url(url, timeout):
        return requests.get(url, timeout=timeout)

    bodies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(load_url, url, 30): url for url in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if len(data.content) > 2:
                bodies.append(data.content)
    return bodies


def get_user_list(user):
    url_list = ['https://myanimelist.net/animelist/{}/load.json?offset={}&status=7'.format(user, i) for i in
                range(0, 300 * 10, 300)]
    bodies = get_bodies(url_list)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    mal_list = []
    for page in content:
        for entry in json.loads(page):
            anime = Anime.query.filter_by(malId=entry['anime_id']).first()
            if anime:
                mal_list.append(get_entry(anime))
    mal_list = sorted(mal_list, key=lambda k: k['title'])
    return mal_list


def get_all_years():
    results = Anime.query.all()
    year_list = []
    for item in results:
        year = item.year
        if year not in year_list:
            year_list.append(year)
    year_list.sort(reverse=True)
    return year_list


def get_all_seasons():
    results = Anime.query.all()
    years = get_all_years()
    year_list = []
    for year in years:
        seasons = []
        for item in results:
            season = item.season[:-5]
            if season not in seasons and str(year) in item.season:
                seasons.append(season)
            if 'All' not in seasons and item.season == 'All' and year == item.year:
                seasons.append("All")
        year_list.append({'year': year, 'seasons': seasons})
    return year_list


def get_year_seasons(year):
    results = Anime.query.filter_by(year=year).all()
    seasons = []
    for item in results:
        season_text = item.season[:-5]
        if season_text not in seasons and len(season_text):
            seasons.append(season_text)
        elif 'All' not in seasons and item.season == 'All':
            seasons.append("All")
    seasons_list = []
    for season in seasons:
        season_list = []
        for item in results:
            if item.season[:-5] == season:
                season_list.append(get_entry(item))
            elif item.season == 'All':
                season_list.append(get_entry(item))
        season_list = sorted(season_list, key=lambda k: k['title'][0])
        seasons_list.append({'season': season, 'animes': season_list})
    seasons_list = sorted(seasons_list, key=lambda k: k['season'])
    return {'year': year, 'seasons': seasons_list}


def get_season(year, season):
    results = Anime.query.filter_by(year=year).all()
    anime_list = []
    for item in results:
        if season.capitalize() in item.season:
            anime_list.append(get_entry(item))
    anime_list = sorted(anime_list, key=lambda k: k['title'][0])
    return anime_list


def get_entry(anime):
    themes = Theme.query.filter_by(mal_id=anime.malId).all()
    theme_list = []
    for theme in themes:
        theme_list.append(theme.json())
    new_list = sorted(theme_list, key=itemgetter('theme_id'), reverse=False)
    return {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover,
            'season': anime.season,
            'year': anime.year, 'themes': new_list}
