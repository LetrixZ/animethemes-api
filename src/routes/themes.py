import json
import string
import subprocess
from subprocess import run, PIPE

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from flask import Blueprint, jsonify, url_for
from werkzeug.utils import redirect

from src.data.repo import theme_list, anime_list, artist_list

theme = Blueprint('theme', __name__)


@theme.route('<string:theme_id>')
def get_theme(theme_id):
    entry = next((item.parse() for item in theme_list if item.theme_id == theme_id), None)
    if theme:
        return jsonify(entry)
    else:
        return jsonify('Theme not found')


@theme.route('<string:theme_id>/mirror')
@theme.route('<string:theme_id>/mirror/<int:index>')
def get_mirror(theme_id, index=0):
    entry = next((item for item in theme_list if item.theme_id == theme_id), None)
    if theme:
        try:
            return jsonify(entry.mirrors[index])
        except IndexError:
            return jsonify({'error': 'invalid index'})


@theme.route('<string:theme_id>/video')
@theme.route('<string:theme_id>/<int:quality>/video')
def get_video(theme_id, quality=0):
    entry = next((item for item in theme_list if item.theme_id == theme_id), None)
    if theme:
        try:
            return redirect(entry['mirrors'][quality]['mirror'])
        except IndexError:
            return jsonify({'error': 'invalid index'})


@theme.route('<string:theme_id>/audio')
@theme.route('<string:theme_id>/<int:quality>/audio')
def get_audio_theme(theme_id, quality=0):
    entry = next((item for item in theme_list if item.theme_id == theme_id), None)
    if theme:
        try:
            mirror = entry.mirrors[quality]
            return redirect(extract_audio(mirror['mirror'], [entry.title, next(
                (item for item in anime_list if item.anime_id == entry.anime_id), None).title.split(' | ')[0],
                                                             entry.type], entry))
        except IndexError:
            return jsonify({'error': 'invalid quality'})
    else:
        return jsonify('Theme not found')


def extract_audio(url, title, entry):
    video_file = ['curl', url, '-o', 'video.webm']
    print(url)
    result = run(video_file, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(result.returncode, result.stdout, result.stderr)
    printable = set(string.printable)
    file_name = ''.join(filter(lambda x: x in printable, title[0]))
    anime_title = ''.join(filter(lambda x: x in printable, title[1]))
    filename = '{} - {} ({}).mp3'.format(file_name, anime_title, title[2])
    print('Encoding')
    try:
        if entry.artist_id:
            artist = f'{next((item.name for item in artist_list if item.artist_id == entry.artist_id), None)} ({next((item.app() for item in anime_list if item.anime_id == entry.anime_id), None)["title"]})' if entry.artist is not None else f'({next((item.app() for item in anime_list if item.anime_id == entry.anime_id), None)["title"]})'
    except:
        artist = ''
    ffmpeg = ['ffmpeg', '-hide_banner', '-i', 'video.webm', '-vn', '-c:a', 'libmp3lame', '-b:a',
              '320k',
              '-metadata', "title='" + title[0] + "'", '-metadata', f"author='{artist}'", filename, "-y"]
    subprocess.run(ffmpeg)
    print('Uploading')
    # file = open(filename, 'rb')
    # data = {'reqtype': 'fileupload', 'userhash': '6e30d558b396c280ace81349f',
    #         'fileToUpload': (file.name, file, 'audio/mp3')}
    # response = multipart_post(data)
    # file.close()
    # print(response.text)
    # return response.text
    payload = {'file': open(filename, 'rb')}
    response = requests.post('https://ki.tc/file/u/', files=payload)
    subprocess.run(['rm', 'video.webm', filename])
    return json.loads(response.content)['file']['link']


def multipart_post(data):
    encoder = MultipartEncoder(fields=data)
    monitor = MultipartEncoderMonitor(encoder)
    r = requests.post("https://catbox.moe/user/api.php", data=monitor, headers={'Content-Type': monitor.content_type})
    return r
