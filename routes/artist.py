import json

from flask import Blueprint, jsonify, request

from routes.themes import theme_list

artist = Blueprint('artist', __name__)
artist_list = json.load(open('data/artist.json', 'r', encoding="utf8"))


def parse_artist(entry, onlyid=0, mobile=0):
    item = entry.copy()
    if mobile == '1':
        item.pop('themes')
        return item
    if onlyid == '1':
        return item
    themes = []
    for theme_id in entry['themes']:
        themes.append([theme for theme in theme_list if theme_id == theme['theme_id']])
    item['themes'] = themes
    return item


@artist.route('<int:artist_id>')
def get_artist(artist_id):
    entry = next((item for item in artist_list if item["artist_id"] == artist_id), None)
    if entry:
        return jsonify(parse_artist(entry, request.args.get('onlyid'), request.args.get('mobile')))
    else:
        return jsonify('Artist not found')
