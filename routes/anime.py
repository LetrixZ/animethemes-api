import json

from flask import Blueprint, jsonify, request

from routes.themes import theme_list

anime = Blueprint('anime', __name__)
anime_list = json.load(open('data/anime.json', 'r', encoding="utf8"))


def parse_anime(entry, only_id=0, mobile=0):
    item = entry.copy()
    if mobile == '1':
        item.pop('themes')
        return item
    if only_id == '1':
        return item
    themes = []
    for theme_id in entry['themes']:
        themes.append([theme for theme in theme_list if theme_id == theme['theme_id']])
    item['themes'] = themes
    return item


@anime.route('<int:anime_id>')
def get_anime(anime_id):
    entry = next((item for item in anime_list if item['anime_id'] == anime_id), None)
    if entry:
        return jsonify(parse_anime(entry, request.args.get('onlyid'), request.args.get('mobile')))
    else:
        return jsonify('Anime not found')
