from django.urls import path

from api.v1.app import *

version = __name__.split('.')[1]

urlpatterns = [
    path('', lambda request: JsonResponse(
        {'message': 'animethemes api', 'author': 'u/LetrixZ', 'docs': 'https://github.com/LetrixZ/animethemes-api'})),

    path('anime/<int:mal_id>', get_anime),
    path('id/<int:mal_id>', themes_by_id),

    path('anime/<int:mal_id>/<str:type>/audio', audio_by_id),
    path('id/<int:mal_id>/<str:type>/audio', audio_by_id),

    path('anime/<int:mal_id>/<str:type>', video_by_id),
    path('id/<int:mal_id>/<str:type>', video_by_id),

    path('s/all/<path:name>', search_all),
    path('s/artist/<path:name>', search_artist),
    path('s/theme/<path:name>', search_theme),
    path('s/anime/<path:name>', search_anime),
    path('s/<path:name>', search_anime),

    path('top', get_top),

    path('anime/<int:mal_id>/<str:theme_index>/<int:version>/audio', get_audio_theme),

    path('anime/<int:mal_id>/<str:theme_index>/<int:version>/video', get_theme),
    path('anime/<int:mal_id>/<str:theme_index>/<int:version>', get_theme),

    path('latest/animes', latest_animes_list),
    path('latest/themes', latest_themes_added),
    path('current', current_season),

    path('anilist/<str:user>', get_anilist),
    path('mal/<path:user>', get_mal_list),
    path('u/<path:user>', get_mal_list),

    path('year/<str:year>', get_year),
    path('seasons', get_seasons),
    path('years', get_years),
    path('seasons/<str:year>', year_seasons),
    path('seasons/<str:year>/<str:season>', season),
]
