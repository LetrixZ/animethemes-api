from operator import itemgetter

import praw, requests, concurrent.futures, json, os
from bs4 import BeautifulSoup
from models import Anime, Theme
from mal import Anime as AnimeMAL

client_secret = os.getenv('CLIENT_SECRET')

reddit = praw.Reddit(client_id="mS1uQkjEv2vxhg",
                     client_secret=client_secret,
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
        anime = AnimeMAL(mal_id)
        image = anime.image_url
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
        themes.append({'title': themeTitle, 'type': themeType, 'mirror': themeMirror, 'episodes': themeEpisodes,
                       'notes': themeNotes, 'extras': {'views': 0, 'likes': 0, 'dislikes': 0, 'malId': malId}})
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
        cover = get_cover(malId)
    return {'malId': malId, 'titles': title, 'themes': themes, 'cover': cover, 'year': year, 'season': season_name}
    # else:
    #    return None


def add_year(year):
    page = reddit.subreddit('AnimeThemes').wiki[year].content_html
    body = BeautifulSoup(page, 'html.parser')
    seasons = body.findAll('h2')
    anime_list = []
    added = []
    if not len(seasons):
        entryList = body.findAll('h3')
        for entry in entryList:
            year = int(str(year).replace('s', ''))
            anime = get_anime(entry, "All", year)
            if anime:
                anime_list.append(anime)
                row = Anime.query.filter_by(malId=anime['malId']).first()
                if not row:
                    added.append(anime)
        return anime_list, added
    for season in seasons:
        season_text = season.getText()
        season_name = season_text[5:season_text.find('Season')] + season_text[:4]
        entryList = []
        item = season
        while True:
            item = item.nextSibling
            if item is None or item.name == 'h2':
                break
            elif item.name == 'h3':
                entryList.append(item)
        for entry in entryList:
            anime = get_anime(entry, season_name, year)
            if anime:
                malId = anime['malId']
                anime_list.append(anime)
                row = Anime.query.filter_by(malId=malId).first()
                if not row:
                    added.append(anime)
                elif row:
                    row_themes = json.loads(row.themes)
                    if row_themes != anime['themes']:
                        added.append(anime)
    return anime_list, added


def getAnimeID(id):
    anime = Anime.query.filter_by(malId=id).first()
    if anime:
        return {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover, 'season': anime.season,
                'year': anime.year, 'themes': json.loads(anime.themes)}
    return None


def getUserList(user):
    url_list = ['https://myanimelist.net/animelist/{}/load.json?offset={}&status=7'.format(user, i) for i in
                range(0, 300 * 10, 300)]
    bodies = getBodies(url_list)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    mal_list = []
    for page in content:
        for entry in json.loads(page):
            anime = Anime.query.filter_by(malId=entry['anime_id']).first()
            if anime:
                mal_list.append(get_entry(anime))
                # themes = Theme.query.filter_by(mal_id=anime.malId).all()
                # theme_list = []
                # for theme in themes:
                #     theme_list.append(theme.json())
                # mal_list.append(
                #     {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover,
                #      'season': anime.season,
                #      'year': anime.year, 'themes': theme_list})
    mal_list = sorted(mal_list, key=lambda k: k['title'])
    return mal_list


def getAllYears():
    results = Anime.query.all()
    year_list = []
    for item in results:
        year = item.year
        if year not in year_list:
            year_list.append(year)
    year_list.sort(reverse=True)
    return year_list


def getAllSeasons():
    results = Anime.query.all()
    years = getAllYears()
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


def getYearSeasons(year):
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


def getCurrentSeason():
    years = getAllSeasons()
    data = list(years[0].values())
    currentSeason = data[1][-1]
    year = data[0]
    return currentSeason, year


def getSeason(year, season):
    results = Anime.query.filter_by(year=year).all()
    anime_list = []
    for item in results:
        if season.capitalize() in item.season:
            anime_list.append(get_entry(item))
    anime_list = sorted(anime_list, key=lambda k: k['title'][0])
    return anime_list


def getCoverFromDB():
    animes = requests.get("https://animethemes-api.herokuapp.com/all/").json()
    for anime in animes:
        row = Anime.query.filter_by(malId=anime['malId']).first()
        if row:
            row.cover = anime['poster']
            row.save()
        else:
            print(" {} ".format(anime['malId'], anime['name']))
    return {'message': 'done'}


def get_entry(anime):
    themes = Theme.query.filter_by(mal_id=anime.malId).all()
    theme_list = []
    for theme in themes:
        theme_list.append(theme.json())
    newlist = sorted(theme_list, key=itemgetter('theme_id'), reverse=False)
    return {'malId': anime.malId, 'title': json.loads(anime.title), 'cover': anime.cover,
            'season': anime.season,
            'year': anime.year, 'themes': newlist}
