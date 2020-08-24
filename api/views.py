from django.http import JsonResponse

from api.models import Anime, Theme, Artist


def api_index(request):
    return JsonResponse({'latest version': 'v2', 'name': 'AnimeThemes unofficial API', 'author': 'u/LetrixZ',
                         'info': 'All data is gathered from r/AnimeThemes. Powered by Django.'})


def stats(request):
    return JsonResponse({'count:': {'anime': Anime.objects.count(),
                                    'themes': Theme.objects.count(),
                                    'artists': Artist.objects.count()}})
