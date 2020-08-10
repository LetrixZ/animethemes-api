import concurrent.futures
import json

import praw
import requests
from bs4 import BeautifulSoup
from mal import Anime as AnimeMAL
from models import Anime, Theme

reddit = praw.Reddit(client_id="mS1uQkjEv2vxhg",
                     client_secret="Vs9q60YyROx780avM7AqsVFzfYM",
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


def get_cover(mal_id):
    row = Anime.query.filter_by(malId=mal_id).first()
    if row and row.cover:
        return row.cover
    else:
        try:
            anime = AnimeMAL(mal_id)
            image = anime.image_url
        except requests.exceptions.ReadTimeout:
            image = None
        return image


def get_themes(table, index, malId, pos, extra):
    themes = []
    for tr in table:
        if not len(tr.findAll('td')[0].getText()):
            continue
        try:
            tr.find('a').get('href')
        except AttributeError:
            continue
        title_column = tr.find('td').getText()
        themeTitle = title_column[title_column.find('"') + 1:-1].replace('\n', '')
        themeType = title_column[:title_column.find(' "')]
        themeMirror = []
        themeQuality = tr.find('a').getText()[tr.find('a').getText().find('ebm (') + 5:-1]
        if not themeQuality:
            themeQuality = 'default'
        themeMirror.append(
            {'quality': themeQuality, 'mirrorUrl': tr.find('a').get('href'),
             'appUrl': '{}/{}/{}'.format(malId, index, 0)})
        try:
            nextMirror = tr.find_next_sibling('tr')
            if not len(nextMirror.findAll('td')[0].getText()):
                themeQuality = nextMirror.find('a').getText()[nextMirror.find('a').getText().find('ebm (') + 5:-1]
                if not themeQuality:
                    themeQuality = 'default'
                themeMirror.append({'quality': themeQuality, 'mirrorUrl': nextMirror.find('a').get('href'),
                                    'appUrl': '{}/{}/{}'.format(malId, index, 1)})
                try:
                    nextMirror_2 = nextMirror.find_next_sibling('tr')
                    if not len(nextMirror_2.findAll('td')[0].getText()):
                        themeQuality = nextMirror_2.find('a').getText()[
                                       nextMirror_2.find('a').getText().find('ebm (') + 5:-1]
                        if not themeQuality:
                            themeQuality = 'default'
                        themeMirror.append({'quality': themeQuality, 'mirrorUrl': nextMirror_2.find('a').get('href'),
                                            'appUrl': '{}/{}/{}'.format(malId, index, 2)})
                except AttributeError:
                    # print('There is not another mirror')
                    pass
        except AttributeError:
            # print('There is not another mirror')
            pass
        themeEpisodes = tr.findAll('td')[2].getText()
        try:
            themeNotes = tr.findAll('td')[3].getText()
        except IndexError:
            themeNotes = ''
        ind = str(index)
        if len(ind) == 1:
            ind = "0" + ind
        if pos is not None and index >= pos:
            if themeNotes:
                Theme.create(themeTitle, themeType, malId, '{}-{}'.format(malId, ind),
                             extra + ", " + themeNotes, 0,
                             json.dumps(themeMirror))
            else:
                Theme.create(themeTitle, themeType, malId, '{}-{}'.format(malId, ind),
                             extra, 0,
                             json.dumps(themeMirror))
        else:
            Theme.create(themeTitle, themeType, malId, '{}-{}'.format(malId, ind), themeNotes, 0,
                         json.dumps(themeMirror))
        themes.append('{}-{}'.format(malId, ind))
        index += 1
    return themes


def add_anime(item, year, season):
    mal_url = item.find('a').get('href')
    if 'myanimelist' not in mal_url:
        return None
    mal_id = int("".join(filter(str.isdigit, mal_url[30:].split('/')[0])))
    row = Anime.query.filter_by(malId=mal_id).first()
    if not row:
        print("not")
        anime_name = item.getText()
        anime_titles = [anime_name]
        try:
            anime_titles.extend(item.nextSibling.nextSibling.find('strong').getText().split(', '))
        except AttributeError:
            pass
        theme_table = item.find_next_sibling('table').find('tbody').findAll('tr')
        pos = len(theme_table)
        entries = theme_table
        # Getting extra themes {
        theme_table_2 = item.find_next_sibling('table')
        extra = ""
        while True:
            theme_table_2 = theme_table_2.nextSibling
            if theme_table_2 is not None and theme_table_2.name == 'p':
                extra = theme_table_2.text
            if theme_table_2 is None or theme_table_2.name == 'h3':
                break
            elif theme_table_2.name == 'table':
                entries += theme_table_2.find('tbody').findAll('tr')
        # }
        themes = get_themes(entries, 0, mal_id, pos, extra)
        cover = get_cover(mal_id)
        return {'malId': mal_id, 'titles': anime_titles, 'themes': themes, 'cover': cover, 'year': year,
                'season': season}
    else:
        theme_table = item.find_next_sibling('table').find('tbody').findAll('tr')
        pos = len(theme_table)
        entries = theme_table
        # Getting extra themes {
        theme_table_2 = item.find_next_sibling('table')
        extra = ""
        while True:
            theme_table_2 = theme_table_2.nextSibling
            if theme_table_2 is not None and theme_table_2.name == 'p':
                extra = theme_table_2.text
            if theme_table_2 is None or theme_table_2.name == 'h3':
                break
            elif theme_table_2.name == 'table':
                entries += theme_table_2.find('tbody').findAll('tr')
        # }
        get_themes(entries, 0, mal_id, pos, extra)


def get_season(entry, year):
    anime_list = []
    for item in entry[1]:
        anime = add_anime(item, year, entry[0])
        if anime:
            anime_list.append(anime)
    return anime_list


def get_year(year):
    page = reddit.subreddit('AnimeThemes').wiki[year].content_html
    body = BeautifulSoup(page, 'html.parser')
    seasons = body.findAll('h2')
    year = int(str(year).replace('s', ''))
    entry_list = {}
    added_list = []
    if not seasons:
        entry_list['All'] = body.findAll('h3')
        for entry in entry_list.items():
            added_list.append(get_season(entry, year))
        return added_list
    for season in seasons:
        season_text = season.getText()
        season_name = season_text[5:season_text.find('Season')] + season_text[:4]
        item = season
        entry_list[season_name] = []
        while True:
            item = item.nextSibling
            if item is None or item.name == 'h2':
                break
            elif item.name == 'h3':
                entry_list[season_name].append(item)
    for entry in entry_list.items():
        print(entry[0])
        season_list = get_season(entry, year)
        added_list.append(season_list)
    return added_list
    # GET ANIME
