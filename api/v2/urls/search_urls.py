from django.urls import path

from api.v2.routes import search

version = __name__.split('.')[1]

urlpatterns = [
    # SEARCH
    path('all/<path:q>', search.search_all, name=f'search-{version}'),
    path('anime/<path:q>', search.search_anime, name=f'search-anime-{version}'),
    path('theme/<path:q>', search.search_theme, name=f'search-theme-{version}'),
    path('artist/<path:q>', search.search_artist, name=f'search-artist-{version}'),

    path('a/<path:q>', search.search_anime, name=f'search-anime-{version}'),
    path('t/<path:q>', search.search_theme, name=f'search-theme-{version}'),
    path('s/<path:q>', search.search_artist, name=f'search-artist-{version}'),
]
