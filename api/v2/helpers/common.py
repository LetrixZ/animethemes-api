import string
import subprocess
from subprocess import PIPE, run

import fileioapi as fileioapi

from api.models import Anime, Theme


def get_latest_list():
    anime_list = Anime.objects.all().order_by('-id')[:15]
    latest_anime_added = []
    for anime in anime_list:
        latest_anime_added.append(anime.json())
    return latest_anime_added


def get_latest_theme_list():
    theme_list = Theme.objects.order_by('-id')[:15]
    latest_themes_list = []
    for theme in theme_list:
        anime = Anime.objects.filter(mal_id=theme.mal_id).first()
        latest_themes_list.append(
            {'mal_id': anime.mal_id, 'title': anime.title[0], 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.json()]})
    return latest_themes_list


def get_top_theme_list():
    theme_list = Theme.objects.order_by('-views')[:15]
    top_list = []
    for theme in theme_list:
        anime = Anime.objects.filter(mal_id=theme.mal_id).first()
        top_list.append(
            {'mal_id': anime.mal_id, 'title': anime.title[0], 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.json()]})
    return top_list


def get_current():
    seasons = ['Fall', 'Summer', 'Spring', 'Winter']
    year = Anime.objects.all().order_by('-year').first().year
    current = 'Winter'
    for i in range(4):
        if Anime.objects.filter(season='{} {}'.format(seasons[i], year)).first():
            current = seasons[i]
            break
    anime_list = Anime.objects.filter(season='{} {}'.format(current, year)).all()
    result_list = []
    for anime in anime_list:
        result_list.append(anime.json())
    return result_list, current, year


def get_audio_file(url, title):
    video = ['curl', url, '-o', 'tmp/video.webm']
    print(url)
    result = run(video, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(result.returncode, result.stdout, result.stderr)
    printable = set(string.printable)
    filename = ''.join(filter(lambda x: x in printable, title[0]))
    anime_title = ''.join(filter(lambda x: x in printable, title[1]))
    filename = '{} - {} ({}).mp3'.format(filename, anime_title, title[2])
    convert_cmd = ['ffmpeg', '-i', 'video.webm', '-vn', '-c:a', 'libmp3lame', '-b:a', '192k', '-metadata', "title='" + title[0] + "'", filename, "-y"]
    subprocess.run(convert_cmd)
    response = fileioapi.upload(filename, "1w")
    subprocess.run(['rm', 'video.webm', filename])
    return response.get("link")
