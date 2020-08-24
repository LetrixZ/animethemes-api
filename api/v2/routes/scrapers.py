import json

import requests
from django.http import JsonResponse

from api.models import Anime, Artist, Theme
from api.v2.scrapers.artist_scraper import get_list
from api.v2.scrapers.reddit_scraper import get_year


def year_scrape(request, year):
    return JsonResponse(get_year(year), safe=False)


def artist_scrape(request):
    return JsonResponse(get_list(), safe=False)


def scrape_anime_covers(request):
    page = requests.get('http://animethemes-api.herokuapp.com/db/print_all/')
    anime_list = json.loads(page.content)
    for anime in anime_list:
        item = Anime.objects.filter(mal_id=anime['malId']).first()
        item.cover = anime['cover']
        item.save()
    return JsonResponse({'message': 'done'})


def scrape_artist_covers(request):
    page = requests.get('http://animethemes-api.herokuapp.com/db/print_all_artist')
    artist_list = json.loads(page.content)
    for artist in artist_list:
        item = Artist.objects.filter(mal_id=artist['mal_id']).first()
        item.cover = artist['cover']
        item.save()
    return JsonResponse({'message': 'done'})


def assign_artist_id(request):
    for artist in Artist.objects.all():
        for theme in artist.themes:
            item = Theme.objects.filter(theme_id=theme).first()
            item.artist_id = artist.mal_id
            item.save()
    return JsonResponse({'message': 'done'})
