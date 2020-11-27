from flask import Blueprint, jsonify

from src.data.repo import anime_list, theme_list, artist_list

search = Blueprint('search', __name__)


@search.route('anime/<path:name>')
def search_anime(name, s_all=False):
    results = [item.parse() for item in anime_list if name.lower() in item.title.lower()]
    if s_all:
        return results
    return jsonify(results)


@search.route('artist/<path:name>')
def search_artist(name, s_all=False):
    results = [item.parse() for item in artist_list if name.lower() in item.name.lower()]
    if s_all:
        return results
    return jsonify(results)


@search.route('theme/<path:name>')
def search_theme(name, s_all=False):
    results = [item.parse() for item in theme_list if name.lower() in item.title.lower()]
    if s_all:
        return results
    return jsonify(results)


@search.route('<path:name>')
def search_all(name):
    return jsonify(
        {'anime': search_anime(name, True), 'themes': search_theme(name, True), 'artist': search_artist(name, True)})
