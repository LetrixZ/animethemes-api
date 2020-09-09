from models import Anime


def get_all_years():
    results = Anime.query.all()
    year_list = []
    for item in results:
        year = item.year
        if year not in year_list:
            year_list.append(year)
    year_list.sort(reverse=True)
    return year_list


def get_all_seasons(year=None):
    results = Anime.query.all()
    if year:
        seasons = []
        for item in results:
            season = item.season[:item.season.find(str(item.year)) - 1]
            if season not in seasons and str(year) in item.season:
                seasons.append(season)
            if 'All' not in seasons and item.season == 'All' and year == item.year:
                seasons.append("All")
        return {'year': year, 'seasons': seasons}
    years = get_all_years()
    year_list = []
    for year in years:
        seasons = []
        for item in results:
            season = item.season[:item.season.find(str(item.year)) - 1]
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
        season_text = item.season[:-4]
        if "All" not in season_text:
            season_text = item.season[:-5]
        if season_text not in seasons and len(season_text):
            seasons.append(season_text)
        elif 'All' not in seasons and item.season == 'All':
            seasons.append("All")
    seasons_list = []
    for season in seasons:
        season_list = []
        for item in results:
            if item.season[:-5] == season or item.season[:-4] == season:
                season_list.append(item.app_json())
            elif item.season == 'All':
                season_list.append(item.app_json())
        season_list = sorted(season_list, key=lambda k: k['title'][0])
        seasons_list.append({'season': season, 'animes': season_list})
    seasons_list = sorted(seasons_list, key=lambda k: k['season'])
    return {'year': year, 'seasons': seasons_list}



def get_season(year, season):
    results = Anime.query.filter_by(year=year).all()
    anime_list = []
    for item in results:
        if season.capitalize() in item.season:
            anime_list.append(item.json())
    anime_list = sorted(anime_list, key=lambda k: k['title'][0])
    return anime_list


def get_current_season():
    seasons = ['Fall', 'Summer', 'Spring', 'Winter']
    year = Anime.query.order_by(Anime.year.desc()).first().year
    current = ''
    for i in range(4):
        if Anime.query.filter_by(season='{} {}'.format(seasons[i], year)).first():
            current = seasons[i]
            break
    anime_list = Anime.query.filter_by(season='{} {}'.format(current, year)).all()
    result_list = []
    for anime in anime_list:
        result_list.append(anime.app_json())
    return result_list
