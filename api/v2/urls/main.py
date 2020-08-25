from django.http import JsonResponse
from django.urls import path, include

from api.v2.routes import scrapers
from api.v2.urls import search_urls, get_urls

version = __name__.split('.')[1]

urlpatterns = [
    path('', lambda request: JsonResponse({'version': version,
                                           'routes': {'Get anime info': 'anime/:mal_id',
                                                      'Get theme info': 'anime/:mal_id/:theme_index',
                                                      'Get theme video': 'anime/:mal_id/:theme_index/:quality_index',
                                                      'Get theme audio': 'anime/:mal_id/:theme_index/audio',
                                                      'Search all': 'search/:query',
                                                      'Search anime': 'search/anime/:query',
                                                      'Search theme': 'search/theme/:query',
                                                      'Search artist': 'search/artist/:query'}})),

    # GET
    path('anime/', include(get_urls)),
    path('id/', include(get_urls)),
    path('mal_id/', include(get_urls)),

    path('search/', include(search_urls)),
    path('find/', include(search_urls)),
    path('s/', include(search_urls)),

    # # SCRAPER
    path('db/year/<str:year>', scrapers.year_scrape),
    path('db/artist', scrapers.artist_scrape),
    # COPY
    path('db/copy/anime', scrapers.scrape_anime_covers),
    path('db/copy/artist', scrapers.scrape_artist_covers),
    # MODIFY
    path('db/modify/artist_id', scrapers.assign_artist_id),
]
