from django.http import JsonResponse
from django.shortcuts import redirect

from api.models import Anime, Theme
from api.v2.helpers.common import get_audio_file


def anime_get(request, mal_id):
    anime = Anime.objects.filter(mal_id=mal_id).first()
    print()
    if anime:
        return JsonResponse(anime.json())
    else:
        return JsonResponse({'message': 'not found'})


def theme_get_info(request, mal_id, theme_index):
    theme_id = f'{mal_id}-{theme_index:02d}'
    theme = Theme.objects.filter(theme_id=theme_id).first()
    print(theme_id)
    if theme:
        return JsonResponse(theme.json())
    else:
        return redirect(f'/api/v2/anime/{mal_id}')


def theme_get_video(request, mal_id, theme_index, theme_quality=0):
    theme_id = f'{mal_id}-{theme_index:02d}'
    theme = Theme.objects.filter(theme_id=theme_id).first()
    print(theme_id)
    if theme:
        try:
            return redirect(theme.json()['mirrors'][theme_quality]['mirror'])
        except IndexError:
            return JsonResponse(theme.json()['mirrors'])
    else:
        return redirect(f'/api/v2/anime/{mal_id}')


def theme_get_audio(request, mal_id, theme_index=0):
    theme_id = f'{mal_id}-{theme_index:02d}'
    theme = Theme.objects.filter(theme_id=theme_id).first()
    print('audio', theme_id)
    if theme:
        anime = Anime.objects.filter(mal_id=mal_id).first()
        try:
            return redirect(
                get_audio_file(theme.json()['mirrors'][0]['mirror'], [theme.title, anime.title[0], theme.type]))
        except IndexError:
            return JsonResponse(theme.json()['mirrors'])
    else:
        return redirect(f'/api/v2/anime/{mal_id}')
