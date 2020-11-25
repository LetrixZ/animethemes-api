import json

from flask import Blueprint, jsonify
from werkzeug.utils import redirect

theme = Blueprint('theme', __name__)
theme_list = json.load(open('data/themes.json', 'r', encoding="utf8"))


@theme.route('<string:theme_id>')
def get_theme(theme_id):
    entry = next((item for item in theme_list if item["theme_id"] == theme_id), None)
    if theme:
        return jsonify(entry)
    else:
        return jsonify('Theme not found')


@theme.route('<string:theme_id>/mirror/')
@theme.route('<string:theme_id>/mirror/<int:index>')
def get_mirror(theme_id, index=0):
    entry = next((item for item in theme_list if item["theme_id"] == theme_id), None)
    if theme:
        try:
            return jsonify(entry['mirrors'][index])
        except IndexError:
            return jsonify({'error': 'invalid index'})


@theme.route('<string:theme_id>/mirror/video')
@theme.route('<string:theme_id>/mirror/<int:index>/video')
def get_video(theme_id, index=0):
    entry = next((item for item in theme_list if item["theme_id"] == theme_id), None)
    if theme:
        try:
            return redirect(entry['mirrors'][index]['mirror'])
        except IndexError:
            return jsonify({'error': 'invalid index'})
