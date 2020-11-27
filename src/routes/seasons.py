from flask import Blueprint, jsonify

from src.data.repo import anime_list

seasons = Blueprint('season', __name__)

season_order = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Fall': 3}


@seasons.route('years')
def list_years():
    return jsonify(sorted(list(set(int(item.year) for item in anime_list))))


@seasons.route('all')
def list_all_seasons():
    year_list = list(set(item.year for item in anime_list if int(item.year) >= 2000))
    year_list.sort()
    season_list = {}
    for year in year_list:
        season_list[year] = sorted(list(set(item.season[:-5] for item in anime_list if item.year == year)),
                                   key=lambda val: season_order[val])
    return jsonify(season_list)


@seasons.route('<int:year>')
@seasons.route('<int:year>/<string:season>')
def list_year_season(year, season=None):
    if season.capitalize() in season_order.keys():
        return jsonify({'year': year, 'season': season.capitalize(),
                        'anime': [item.parse() for item in anime_list if
                                  item.year == str(year) and season.capitalize() in item.season]})
    if year >= 2000:
        season_list = sorted(list(set(item.season[:-5] for item in anime_list if item.year == str(year))),
                             key=lambda val: season_order[val])
        tmp_list = []
        for season in season_list:
            tmp_list.append({'season': season, 'anime': [item.parse() for item in anime_list if
                                                         item.year == str(year) and season in item.season]})
            return jsonify({'year': year, 'seasons': tmp_list})