import praw, requests, concurrent.futures, json
from bs4 import BeautifulSoup
from models import Anime, db, Theme
from mal import Anime as AnimeMAL

reddit = praw.Reddit(client_id="mS1uQkjEv2vxhg",
                     client_secret="Vs9q60YyROx780avM7AqsVFzfYM",
                     user_agent="Letrix's AnimeThemes API")


def getBodies(urlList):
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


def get_themes(table, index, malId):
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
        Theme.create(themeTitle, themeType, malId, '{}-{}'.format(malId, index), themeNotes, 0, json.dumps(themeMirror))
        # themes.append({'title': themeTitle, 'type': themeType, 'mirror': themeMirror, 'episodes': themeEpisodes,
        #                'notes': themeNotes, 'extras': {'views': 0, 'likes': 0, 'dislikes': 0, 'malId': malId}})
        themes.append({'theme_title': themeTitle, 'theme_id': '{}-{}'.format(malId, index)})
        index += 1
    return themes


def get_anime(entry, season_name, year):
    index = 0
    malUrl = entry.find('a').get('href')
    if 'myanimelist' not in malUrl:
        return None
    malId = malUrl[30:]
    malId = malId.split('/')[0]
    malId = int("".join(filter(str.isdigit, malId)))
    name = entry.getText()
    title = [name]
    try:
        title.extend(entry.nextSibling.nextSibling.find('strong').getText().split(', '))
    except AttributeError:
        # print('There are not another titles')
        pass
    table = entry.find_next_sibling('table').find('tbody').findAll('tr')
    themes = get_themes(table, index, malId)
    table2 = entry.find_next_sibling('table')
    while True:
        table2 = table2.nextSibling
        if table2 is None or table2.name == 'h3':
            break
        elif table2.name == 'table':
            themes += get_themes(table2.find('tbody').findAll('tr'), index, malId)
    row = Anime.query.filter_by(malId=malId).first()
    if row:
        cover = row.cover
    else:
        # cover = get_cover(malId)
        cover = None
    return {'malId': malId, 'titles': title, 'themes': themes, 'cover': cover, 'year': year, 'season': season_name}
    # else:
    #    return None


def add_anime(item, year, season):
    mal_url = item.find('a').get('href')
    if 'myanimelist' not in mal_url:
        return None
    mal_id = int("".join(filter(str.isdigit, mal_url[30:].split('/')[0])))
    row = Anime.query.filter_by(malId=mal_id).first()
    if not row:
        anime_name = item.getText()
        anime_titles = [anime_name]
        try:
            anime_titles.extend(item.nextSibling.nextSibling.find('strong').getText().split(', '))
        except AttributeError:
            pass
        theme_table = item.find_next_sibling('table').find('tbody').findAll('tr')
        themes = get_themes(theme_table, 0, mal_id)
        # Getting extra themes {
        theme_table_2 = item.find_next_sibling('table')
        while True:
            theme_table_2 = theme_table_2.nextSibling
            if theme_table_2 is None or theme_table_2.name == 'h3':
                break
            elif theme_table_2.name == 'table':
                themes += get_themes(theme_table_2.find('tbody').findAll('tr'), 0, mal_id)
        # }
        cover = get_cover(mal_id)
        # cover = None
        return {'malId': mal_id, 'titles': anime_titles, 'themes': themes, 'cover': cover, 'year': year,
                'season': season}
    else:
        themes = Theme.query.filter_by(mal_id=mal_id).all()
        theme_table = item.find_next_sibling('table').find('tbody').findAll('tr')
        new_themes = get_themes(theme_table, 0, mal_id)
        theme_table_2 = item.find_next_sibling('table')
        while True:
            theme_table_2 = theme_table_2.nextSibling
            if theme_table_2 is None or theme_table_2.name == 'h3':
                break
            elif theme_table_2.name == 'table':
                new_themes += get_themes(theme_table_2.find('tbody').findAll('tr'), 0, mal_id)
        # if len(themes) != len(new_themes):
        #     print("{}, different list".format(json.loads(row.title)[0]))
        #     for theme in new_themes:
        #         print(theme.get('title'))
        # for i in range(len(themes)):
        #     if len(themes[i].json().get('mirror')) != len(new_themes[i].get('mirror')):
        #         print(json.loads(row.title))
        #         print('{}, different mirrors'.format(themes[i].get('title')))
        #         themes[i]['mirror'] = new_themes[i]['mirror']
        if len(new_themes) != len(new_themes):
            print("{}, different lists".format(json.loads(row.title)[0]))
        # for i in range(len(themes)):
        #     print(len(json.loads(themes[i].mirrors)))
        #     if len(new_themes[i].get('mirror')) != len(json.loads(themes[i].mirrors)):
        #         print('{}, different mirrors'.format(themes[i].title))


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
