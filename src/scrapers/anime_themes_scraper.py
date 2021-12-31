import dataclasses
import json

import praw
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from mal import Anime as AnimeMAL

from models import Anime, Theme, object_decoder

load_dotenv()

reddit = praw.Reddit(client_id=os.getenv('PRAW_CLIENT_ID'),
                     client_secret=os.getenv('PRAW_CLIENT_SECRET'),
                     user_agent="Letrix's AnimeThemes API")


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


local_anime_list = json.load(open('src/data/anime.json', 'r', encoding="utf8"), object_hook=object_decoder)
local_theme_list = json.load(open('src/data/themes.json', 'r', encoding="utf8"), object_hook=object_decoder)


def get_cover(mal_id):
    try:
        anime = AnimeMAL(mal_id)
        image = anime.image_url
    except requests.exceptions.ReadTimeout:
        image = None
    except TypeError:
        image = None
    return image


def get_mal_id(link):
    if 'myanimelist' in link:
        tmp = link.split('/')
        if tmp[-1]:
            try:
                return int(tmp[-1])
            except ValueError:
                return int(tmp[-2])
        elif tmp[-2]:
            try:
                return int(tmp[-2])
            except ValueError:
                return int(tmp[-3])
    else:
        print(link)
        return None


def get_theme(entry, mal_id, theme_id, category, theme_list_db):
    if entry.find('td').text:
        try:
            title = entry.find('td').text.split(' "')[1][:-1]
        except IndexError:
            title = entry.find('td').text.split('"')[1][:-1]
        type = entry.find('td').text.split(' "')[0]
        mirror_info = entry.findAll('td')[1].find('a')
        if not mirror_info:
            return
        mirrors = [{'quality': mirror_info.text.partition("(")[2].partition(")")[0],
                    'mirror': mirror_info.get('href')}]
        episodes = entry.findAll('td')[2].text
        try:
            notes = entry.findAll('td')[3].text
        except IndexError:
            episodes = ""
            notes = entry.findAll('td')[2].text
        # Next mirror
        next_mirror = entry.nextSibling.nextSibling
        if next_mirror and next_mirror.name == 'tr':
            if next_mirror.find('td').text == '':
                mirror_info = next_mirror.findAll('td')[1].find('a')
                mirrors.append({'quality': mirror_info.text.partition("(")[2].partition(")")[0],
                                'mirror': mirror_info.get('href')})
        # Next mirror
        try:
            next_mirror = next_mirror.nextSibling.nextSibling
            if next_mirror and next_mirror.name == 'tr':
                if next_mirror.find('td').text == '':
                    mirror_info = next_mirror.findAll('td')[1].find('a')
                    mirrors.append({'quality': mirror_info.text.partition("(")[2].partition(")")[0],
                                    'mirror': mirror_info.get('href')})
        except:
            pass
        theme = Theme(mal_id, None, theme_id, title, type, notes,
                      episodes, category, mirrors)
        if theme:
            if theme not in local_theme_list:
                print(f'New theme {theme.theme_id}: {theme.title}')
                theme_list_db.append(theme)
            else:
                db_theme = next(
                    (index for index, item in enumerate(local_theme_list) if item.theme_id == theme.theme_id),
                    None)
                if db_theme and local_theme_list[db_theme].mirrors != theme.mirrors or local_theme_list[
                    db_theme].episodes != theme.episodes:
                    print(f'Updating theme with index = {db_theme}, id = {theme.theme_id}, name = {theme.title}')
                    local_theme_list[db_theme] = theme
                    with open("src/data/themes.json", 'w') as f:
                        json.dump(local_theme_list, f, cls=EnhancedJSONEncoder)
        return {'title': title, 'type': type, 'episodes': episodes, 'notes': notes,
                'category': category, 'mirrors': mirrors}


def get_anime(entry, year, season, theme_list_db):
    mal_id = get_mal_id(entry.find('a').get('href'))
    if mal_id:
        theme_list = []
        title = [entry.text]
        entry = entry.nextSibling.nextSibling
        # Extra names
        if entry.name == 'p':
            title.extend(entry.text.split(', '))
            entry = entry.nextSibling.nextSibling
        category = ""
        if entry.name == 'p':
            category = entry.text
            entry = entry.nextSibling.nextSibling
        theme_size = 0
        for index, item in enumerate(entry.findAll('tr')[1:]):
            if item.find('td').text != "":
                theme = get_theme(item, mal_id, f'{mal_id}-{f"{theme_size:02d}"}', category, theme_list_db)
                if theme:
                    theme_list.append(f'{mal_id}-{f"{theme_size:02d}"}')
                theme_size += 1
        entry = entry.nextSibling.nextSibling
        if entry:
            if entry.name == 'p':
                category = entry.text
                entry = entry.nextSibling.nextSibling
            for index, item in enumerate(entry.findAll('tr')[1:], start=theme_size):
                theme = get_theme(item, mal_id, f'{mal_id}-{f"{index:02d}"}', category, theme_list_db)
                if theme:
                    theme_list.append(f'{mal_id}-{f"{theme_size:02d}"}')
        return Anime(mal_id, ' | '.join(title), None, year, season,
                     theme_list)
    else:
        return None


def get_year(year):
    anime_list = []
    theme_list = []
    page = BeautifulSoup(reddit.subreddit('AnimeThemes').wiki[year].content_html, 'html.parser')
    print(year)
    if page.findAll('h2'):
        for item in page.findAll('h2'):
            season = f'{item.text.split(" ")[1]} {int(str(year).replace("s", ""))}'
            aux = item
            while True:
                aux = aux.nextSibling
                if aux is None or aux.name == 'h2':
                    break
                elif aux.name == 'h3':
                    anime = get_anime(aux, year, season, theme_list)
                    if anime:
                        if anime not in local_anime_list:
                            print(f'New anime {anime.anime_id}: {anime.title}')
                            anime_list.append(anime)
                        else:
                            db_anime = next((index for index, item in enumerate(local_anime_list) if
                                             item.anime_id == anime.anime_id), None)
                            if db_anime and local_anime_list[db_anime].themes != anime.themes:
                                print(
                                    f'Updating anime with index {db_anime}, anime_id = {anime.anime_id}, title = {anime.title}')
                                local_anime_list[db_anime] = anime
                                with open("src/data/anime.json", 'w') as f:
                                    json.dump(local_anime_list, f, cls=EnhancedJSONEncoder)
    else:
        season = f'All {year}'
        year = int(str(year).replace('s', ''))
        for entry in page.findAll('h3'):
            anime = get_anime(entry, year, season, theme_list)
            if anime:
                if anime not in local_anime_list:
                    print(f'New anime {anime.anime_id}: {anime.title}')
                    anime_list.append(anime)
                else:
                    db_anime = next((index for index, item in enumerate(local_anime_list) if
                                     item.anime_id == anime.anime_id), None)
                    if db_anime and local_anime_list[db_anime].themes != anime.themes:
                        print(
                            f'Updating anime with index {db_anime}, anime_id = {anime.anime_id}, title = {anime.title}')
                        local_anime_list[db_anime] = anime
                        with open("src/data/anime.json", 'w') as f:
                            json.dump(local_anime_list, f, cls=EnhancedJSONEncoder)
    return anime_list, theme_list
