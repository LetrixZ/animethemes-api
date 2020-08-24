from django.db.models import Q
from django.http import JsonResponse

from api.models import Anime, Theme, Artist


def search_all(request, q):
    return JsonResponse({'anime_list': search_anime(None, q),
                         'theme_list': search_theme(None, q),
                         'artist_list': search_artist(None, q)})


def search_anime(request, q):
    query_list = Anime.objects.filter(Q(title__icontains=q)).distinct()
    anime_list = []
    for anime in query_list:
        anime_list.append(anime.json())
    if request:
        return JsonResponse(anime_list, safe=False)
    else:
        return anime_list


def search_theme(request, q):
    query_list = Theme.objects.filter(Q(title__icontains=q)).distinct()
    theme_list = []
    for theme in query_list:
        theme_list.append(theme.json())
    if request:
        return JsonResponse(theme_list, safe=False)
    else:
        return theme_list


def search_artist(request, q):
    query_list = Artist.objects.filter(Q(name__icontains=q)).distinct()
    artist_list = []
    for artist in query_list:
        artist_list.append(artist.json())
    if request:
        return JsonResponse(artist_list, safe=False)
    else:
        return artist_list
