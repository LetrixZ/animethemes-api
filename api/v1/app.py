import string
import subprocess
from subprocess import PIPE, run

import fileioapi as fileioapi
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect

from api.models import Anime, Theme
from api.models import Artist
from api.v1.anilist import getListFromUser
from api.v1.scrapers import get_user_list, get_all_years, get_all_seasons, get_year_seasons, get_season, \
    get_entry


# GENERAL ROUTES

def get_anime(request, mal_id):
    anime = Anime.objects.filter(mal_id=mal_id).first()
    if anime:
        return JsonResponse(get_entry(anime))
    else:
        return JsonResponse({'message': 'anime not found'})


def season(request, year, season):
    year = year.replace('s', '')
    return JsonResponse(get_season(year, season))


def year_seasons(request, year):
    year = year.replace('s', '')
    return JsonResponse(get_year_seasons(year))


def get_years(request):
    return JsonResponse(get_all_years())


def get_seasons(request):
    return JsonResponse(get_all_seasons())


def get_year(request, year):
    year = int(str(year).replace('s', ''))
    results = Anime.objects.filter(year=year).all()
    anime_list = []
    for anime in results:
        anime_list.append(get_entry(anime))
    return JsonResponse(anime_list)


def get_mal_list(request, user):
    mal_list = get_user_list(user)
    return JsonResponse(mal_list)


def get_anilist(request, user):
    ani_list = getListFromUser(user)
    anime_list = []
    for item in ani_list:
        mal_id = item['media']['idMal']
        anime = Anime.objects.filter(mal_id=mal_id).first()
        if anime:
            anime_list.append(get_entry(anime))
    anime_list = sorted(anime_list, key=lambda k: k['title'])
    return JsonResponse(anime_list)


def current_season(request):
    seasons = ['Fall', 'Summer', 'Spring', 'Winter']
    year = Anime.objects.order_by('-year')[:15]
    current = 'Winter'
    for i in range(4):
        if Anime.objects.filter(season='{} {}'.format(seasons[i], year)).first():
            current = seasons[i]
            break
    anime_list = Anime.objects.filter(season='{} {}'.format(current, year)).all()
    result_list = []
    for anime in anime_list:
        result_list.append(get_entry(anime))
    return JsonResponse(result_list)


def latest_themes_added(request):
    theme_list = Theme.objects.order_by('-id')[:15]
    result_list = []
    for theme in theme_list:
        anime = Anime.objects.filter(mal_id=theme.mal_id).first()
        result_list.append(
            {'malId': anime.malId, 'title': anime.title, 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.v1_json()]})
    return JsonResponse(result_list)


def latest_animes_list(request):
    anime_list = Anime.objects.order_by('-id')[:15]
    result_list = []
    for anime in anime_list:
        result_list.append(get_entry(anime))
    return JsonResponse(result_list)


def get_theme(request, mal_id, theme_index, version):
    anime = Anime.objects.filter(mal_id=mal_id).first()
    if len(theme_index) == 1:
        theme_index = '0' + theme_index
    if anime:
        theme = Theme.objects.filter(theme_id='{}-{}'.format(mal_id, theme_index)).first()
        if theme:
            try:
                return redirect(theme.mirrors[version].get('mirror'))
            except IndexError:
                return JsonResponse({'message': 'error bad index'})
        else:
            return JsonResponse({'message': 'bad index'})
    else:
        return JsonResponse({'message': 'anime not found'})


def get_audio_theme(request, mal_id, theme_index, version):
    anime = Anime.objects.filter(mal_id=mal_id).first()
    if len(theme_index) == 1:
        theme_index = '0' + theme_index
    theme = Theme.objects.filter(theme_id='{}-{}'.format(mal_id, theme_index)).first()
    if theme:
        title = [theme.title, anime.title[0], theme.type]
        mirrors = theme.mirrors
        url = mirrors[version].get('mirror')
        return redirect(getAudio(url, title))
    else:
        return redirect("api/v1/anime/{}".format(id))


def get_top(request):
    theme_list = Theme.objects.order_by('-views')[:15]
    result_list = []
    for theme in theme_list:
        anime = Anime.objects.filter(mal_id=theme.mal_id).first()
        result_list.append(
            {'malId': anime.malId, 'title': anime.title, 'cover': anime.cover, 'season': anime.season,
             'year': anime.year, 'themes': [theme.v1_json()]})
    return JsonResponse(result_list)


def search_theme(request, name):
    results = Theme.objects.filter(Q(title__icontains=name)).distinct()
    search_list = []
    for item in results:
        search_list.append(item.single_json())
    return JsonResponse(search_list)


def search_anime(request, name):
    results = Anime.objects.filter(Q(title__icontains=name)).distinct()
    animeList = []
    for item in results:
        animeList.append(get_entry(item))
    return JsonResponse(animeList)


def search_artist(request, name):
    results = Artist.objects.filter(Q(name__icontains=name)).distinct()
    artist_list = []
    for item in results:
        artist_list.append(item.v1_json())
    return JsonResponse(artist_list)


def search_all(request, name):
    theme_query = Theme.objects.filter(Q(title__icontains=name)).distinct()
    theme_list = []
    for theme in theme_query:
        theme_list.append(theme.single_json())

    anime_query = Anime.objects.filter(Q(title__icontains=name)).distinct()
    anime_list = []
    for anime in anime_query:
        anime_list.append(get_entry(anime))

    artist_query = Artist.objects.filter(Q(name__icontains=name)).distinct()
    artist_list = []
    for artist in artist_query:
        artist_list.append(artist.v1_json())

    return JsonResponse({'anime_list': {'animeList': anime_list, 'title': 'Anime', 'type': 0},
                         'theme_list': {'animeList': theme_list, 'title': 'Theme', 'type': 1},
                         'artist_list': artist_list})


# LEGACY ROUTES

def getAudio(url, title):
    videoFile = ['curl', url, '-o', 'video.webm']
    print(url)
    # subprocess.run(videoFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = run(videoFile, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(result.returncode, result.stdout, result.stderr)
    printable = set(string.printable)
    fileTitle = ''.join(filter(lambda x: x in printable, title[0]))
    animeTitle = ''.join(filter(lambda x: x in printable, title[1]))
    filename = '{} - {} ({}).mp3'.format(fileTitle, animeTitle, title[2])
    ffmpeg = ['ffmpeg', '-i', 'video.webm', '-vn', '-c:a', 'libmp3lame', '-b:a', '320k',
              '-metadata', "title='" + title[0] + "'", filename, "-y"]
    subprocess.run(ffmpeg)
    response = fileioapi.upload(filename, "1w")
    subprocess.run(['rm', 'video.webm', filename])
    return response.get("link")


def video_by_id(request, mal_id, type):
    type = type.lower()
    anime = Anime.objects.filter(mal_id=mal_id).first()
    themes = Theme.objects.filter(mal_id=mal_id).all()
    for theme in themes:
        if theme.type.lower() == type:
            return redirect(theme.mirrors[0]['mirror'])
    return redirect("api/v1/id/{}".format(mal_id))


def audio_by_id(request, mal_id, type):
    type = type.lower()
    anime = Anime.objects.filter(mal_id=mal_id).first()
    themes = Theme.objects.filter(mal_id=mal_id).all()
    for theme in themes:
        if theme.type.lower() == type:
            title = [theme.title, anime.title[0], theme.type]
            url = theme.mirrors[0]['mirror']
            return redirect(getAudio(url, title))
    return redirect("api/v1/id/{}".format(mal_id))


def themes_by_id(request, mal_id):
    entry = Anime.objects.filter(mal_id=mal_id).first()
    if entry is None:
        return JsonResponse(
            {'message': "this anime isn't available in r/AnimeThemes. Send me a message if it is to u/LetrixZ"})
    anime = get_entry(entry)
    return JsonResponse(anime)
