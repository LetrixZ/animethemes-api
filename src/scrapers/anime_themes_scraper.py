import praw
import requests
import os
from bs4 import BeautifulSoup
from mal import Anime as AnimeMAL

from src.models import Anime, Theme

reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent="Letrix's AnimeThemes API")


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
        mirrors = [{'quality': mirror_info.text.partition("(")[2].partition(")")[0].split(', '),
                    'mirror': mirror_info.get('href')}]
        episodes = entry.findAll('td')[2].text
        try:
            notes = entry.findAll('td')[3].text
        except IndexError:
            episodes = ""
            notes = entry.findAll('td')[2].text
        # Next mirror
        next = entry.nextSibling.nextSibling
        if next and next.name == 'tr':
            if next.find('td').text == '':
                mirror_info = next.findAll('td')[1].find('a')
                mirrors.append({'quality': mirror_info.text.partition("(")[2].partition(")")[0].split(', '),
                                'mirror': mirror_info.get('href')})
        # Next mirror
        try:
            next = next.nextSibling.nextSibling
            if next and next.name == 'tr':
                if next.find('td').text == '':
                    mirror_info = next.findAll('td')[1].find('a')
                    mirrors.append({'quality': mirror_info.text.partition("(")[2].partition(")")[0].split(', '),
                                    'mirror': mirror_info.get('href')})
        except:
            pass
        theme_list_db.append(Theme(mal_id, None, theme_id, title, type, notes,
                                   episodes, category, mirrors))
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
                        anime_list.append(anime)
    else:
        season = f'All {year}'
        year = int(str(year).replace('s', ''))
        for entry in page.findAll('h3'):
            anime = get_anime(entry, year, season, theme_list)
            if anime:
                anime_list.append(anime)
    return anime_list, theme_list
