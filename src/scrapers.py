import praw, requests, concurrent.futures, json
from bs4 import BeautifulSoup
from models import Anime
from mal import Anime as AnimeMAL

reddit = praw.Reddit(client_id="mS1uQkjEv2vxhg", client_secret="Vs9q60YyROx780avM7AqsVFzfYM", user_agent="Letrix's AnimeThemes API")

def getBodies(urlList):
    def load_url(url, timeout):
        return requests.get(url, timeout = timeout)
    bodies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(load_url, url, 30): url for url in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if (len(data.content) > 2):
                bodies.append(data.content)
    return bodies

def getCover(id):
    row = Anime.query.filter_by(malId=id).first()
    if row and row.cover:
        return row.cover
    else:
        print(id)
        anime = AnimeMAL(id)
        image = anime.image_url
        """try:
            request = session.anime(id)
            image = request.picture
        except:
            print(id)
            raise SystemExit(0)
            image = None"""
        return image

def getThemes(table):
    themes = []
    for tr in table:
        if not len(tr.findAll('td')[0].getText()):
            continue
        try:
            tr.find('a').get('href')
        except AttributeError:
            continue
        titleColumn = tr.find('td').getText()
        themeTitle = titleColumn[titleColumn.find('"')+1:-1].replace('\n', '')
        themeType = titleColumn[:titleColumn.find(' "')]
        themeMirror = []
        themeQuality = tr.find('a').getText()[tr.find('a').getText().find('ebm (')+5:-1]
        if not themeQuality:
            themeQuality = 'default'
        themeMirror.append({'quality':themeQuality,'mirrorUrl': tr.find('a').get('href')})
        try:
            nextMirror = tr.find_next_sibling('tr')
            if not len(nextMirror.findAll('td')[0].getText()):
                themeQuality = nextMirror.find('a').getText()[nextMirror.find('a').getText().find('ebm (')+5:-1]
                if not themeQuality:
                    themeQuality = 'default'
                themeMirror.append({'quality':themeQuality,'mirrorUrl': nextMirror.find('a').get('href')})
        except AttributeError:
            #print('There is not another mirror')
            None
        themeEpisodes = tr.findAll('td')[2].getText()
        try:
            themeNotes = tr.findAll('td')[3].getText()
        except IndexError:
            themeNotes = ''
        themes.append({'title':themeTitle, 'type': themeType, 'mirror': themeMirror, 'episodes': themeEpisodes, 'notes': themeNotes})
    return themes

def getAnime(entry, seasonName, year):
    malUrl = entry.find('a').get('href')
    if not 'myanimelist' in malUrl:
        return None
    malId = malUrl[30:]
    malId = malId.split('/')[0]
    malId = int("".join(filter(str.isdigit, malId)))
    name = entry.getText()
    title = [name]
    try:
        title.extend(entry.nextSibling.nextSibling.find('strong').getText().split(', '))
    except AttributeError:
        #print('There are not another titles')
        None
    table = entry.find_next_sibling('table').find('tbody').findAll('tr')
    themes = getThemes(table)
    cover = getCover(malId)
    return {'malId':malId,'titles':title,'themes':themes, 'cover':cover, 'year':year, 'season':seasonName}

def addYear(year):
    page = reddit.subreddit('AnimeThemes').wiki[year].content_html
    body = BeautifulSoup(page, 'html.parser')
    seasons = body.findAll('h2')
    animeList = []
    if not len(seasons):
        entryList = body.findAll('h3')
        for entry in entryList:
            year = int(str(year).replace('s',''))
            anime = getAnime(entry, "All", year)
            row = Anime.query.filter_by(malId=anime['malId']).first()
            if anime:
                if not row:
                    print(row.malId)
                    animeList.append(anime)
        return animeList
    for season in seasons:
        seasonText = season.getText()
        seasonName = seasonText[5:seasonText.find('Season')]+seasonText[:4]
        entryList = []
        item = season
        while True:
            item = item.nextSibling
            if item is None or item.name == 'h2':
                break
            elif item.name == 'h3':
                entryList.append(item)
        for entry in entryList:
            anime = getAnime(entry, seasonName, year)
            row = Anime.query.filter_by(malId=anime['malId']).first()

            if anime:
                if not row:
                    print(row.malId)
                    animeList.append(anime)
    return animeList

def getAnimeID(id):
    anime = Anime.query.filter_by(malId=id).first()
    if anime:
        return {'malId':anime.malId, 'title':json.loads(anime.title), 'cover':anime.cover, 'season':anime.season, 'year':anime.year, 'themes':json.loads(anime.themes)}
    return None

def getUserList(user):
    urlList = ['https://myanimelist.net/animelist/{}/load.json?offset={}&status=7'.format(user, i) for i in range(0, 300*4, 300)]
    bodies = getBodies(urlList)
    content = []
    for body in bodies:
        content.append(body.decode("utf-8"))
    malList = []
    for page in content:
        for entry in json.loads(page):
            anime = getAnimeID(entry['anime_id'])
            if anime:
                malList.append(anime)
    malList = sorted(malList, key=lambda k: k['title']) 
    return malList

def getAllYears():
    results = Anime.query.all()
    yearList = []
    for item in results:
        year = item.year
        if year not in yearList:
            yearList.append(year)
    yearList.sort(reverse=True)
    return yearList

def getAllSeasons():
    results = Anime.query.all()
    years = getAllYears()
    yearList = []
    for year in years:
        seasons = []
        for item in results:
            season = item.season[:-5]             
            if season not in seasons and str(year) in item.season:
                seasons.append(season)
            if 'All' not in seasons and item.season == 'All' and year == item.year:
                seasons.append("All")
        yearList.append({'year':year,'seasons':seasons})
    return yearList

def getYearSeasons(year):
    results = Anime.query.filter_by(year=year).all()
    seasons = []
    for item in results:
        seasonText = item.season[:-5]
        if seasonText not in seasons and len(seasonText):
                seasons.append(seasonText)
        elif 'All' not in seasons and item.season == 'All':
            seasons.append("All")
    seasonsList = []
    for season in seasons:
        seasonList = []
        for item in results:
            if item.season[:-5] == season:
                seasonList.append(item.json())
            elif item.season == 'All':
                seasonList.append(item.json())
        seasonList = sorted(seasonList, key=lambda k: k['title'][0])
        seasonsList.append({'season':season, 'animes': seasonList})
    seasonsList = sorted(seasonsList, key=lambda k: k['season'])
    return {'year':year,'seasons':seasonsList}

def getCurrentSeason():
    years = getAllSeasons()
    data = list(years[0].values())
    currentSeason = data[1][0]
    year = data[0]
    return (currentSeason, year)

def getSeason(year, season):
    results = Anime.query.filter_by(year=year).all()
    animeList = []
    for item in results:
        if season.capitalize() in item.season:
            animeList.append(item.json())
    animeList = sorted(animeList, key=lambda k: k['title'][0])
    return animeList