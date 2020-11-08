import string
import subprocess
from subprocess import run, PIPE

import fileioapi
import requests
from flask import Blueprint, redirect, url_for, jsonify

from models import Anime, Theme

anime = Blueprint('anime', __name__)


@anime.route('<int:mal_id>')
def get_anime(mal_id):
    item = Anime.query.filter_by(mal_id=mal_id).first()
    if item:
        return jsonify(item.json())
    else:
        return jsonify({'error': 'anime not in database'})


@anime.route('<int:mal_id>/<int:theme_index>')
def theme_info(mal_id, theme_index):
    item = Anime.query.filter_by(mal_id=mal_id).first()
    theme = item.themes[theme_index]
    if theme:
        theme['cover'] = item.cover
        theme['name'] = item.title[0]
        return jsonify(theme)
    else:
        return jsonify({'error': 'theme not in database'})


@anime.route('<int:mal_id>/<int:theme_index>/<int:quality>/video')
@anime.route('<int:mal_id>/<int:theme_index>/video')
def get_video(mal_id, theme_index, quality=0):
    theme = Theme.query.filter_by(theme_id=f'{mal_id}-{theme_index:02d}').first()
    # item = Anime.query.filter_by(mal_id=mal_id).first()
    # theme = item.themes[theme_index]
    if theme:
        try:
            mirror = theme.mirrors[quality]
            return redirect(mirror['mirror'])
        except IndexError:
            return jsonify({'error': 'invalid quality'})
    else:
        return redirect(url_for('anime.get_anime', mal_id=mal_id))


@anime.route('<int:mal_id>/<int:theme_index>/<int:quality>/audio')
@anime.route('<int:mal_id>/<int:theme_index>/audio')
def get_audio_theme(mal_id, theme_index, quality=0):
    theme = Theme.query.filter_by(theme_id=f'{mal_id}-{theme_index:02d}').first()
    # item = Anime.query.filter_by(mal_id=mal_id).first()
    # theme = item.themes[theme_index]
    if theme:
        try:
            mirror = theme.mirrors[quality]
            return redirect(extract_audio(mirror['mirror'],
                                          [theme['title'], Anime.query.filter_by(mal_id=mal_id).first().title[0],
                                           theme['type']]))
        except IndexError:
            return jsonify({'error': 'invalid quality'})
    else:
        return redirect(url_for('anime.get_anime', mal_id=mal_id))


def extract_audio(url, title):
    video_file = ['curl', url, '-o', 'video.webm']
    print(url)
    result = run(video_file, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(result.returncode, result.stdout, result.stderr)
    printable = set(string.printable)
    file_name = ''.join(filter(lambda x: x in printable, title[0]))
    anime_title = ''.join(filter(lambda x: x in printable, title[1]))
    filename = '{} - {} ({}).mp3'.format(file_name, anime_title, title[2])
    ffmpeg = ['ffmpeg', '-i', 'video.webm', '-vn', '-c:a', 'libmp3lame', '-b:a', '320k',
              '-metadata', "title='" + title[0] + "'", filename, "-y"]
    subprocess.run(ffmpeg)
    # file_upload = ['curl', '-F', f'"file=@{filename}"', 'https://file.io']
    # upload_result = subprocess.run(file_upload)
    # response = fileioapi.upload(filename, "1w")
    payload = {'file': open(filename, 'rb')}
    response = requests.post('https://ki.tc/file/u/', files=payload)
    subprocess.run(['rm', 'video.webm', filename])
    return response.content.get("link")
