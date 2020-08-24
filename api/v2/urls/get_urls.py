from django.urls import path

from api.v2.routes import main

version = __name__.split('.')[1]

urlpatterns = [
    path('<int:mal_id>', main.anime_get, name=f'anime-{version}'),
    path('<int:mal_id>/<int:theme_index>', main.theme_get_info),
    path('<int:mal_id>/<int:theme_index>/<int:theme_quality>', main.theme_get_video),

    # VIDEO
    path('<int:mal_id>/<int:theme_index>/video', main.theme_get_video),
    path('<int:mal_id>/<int:theme_index>/v', main.theme_get_video),
    path('<int:mal_id>/<int:theme_index>/<int:theme_quality>/video', main.theme_get_video),
    path('<int:mal_id>/<int:theme_index>/<int:theme_quality>/v', main.theme_get_video),

    # AUDIO
    path('<int:mal_id>/<int:theme_index>/audio', main.theme_get_audio),
    path('<int:mal_id>/<int:theme_index>/a', main.theme_get_audio),
    path('<int:mal_id>/<int:theme_index>/<int:theme_quality>/audio', main.theme_get_audio),
    path('<int:mal_id>/<int:theme_index>/<int:theme_quality>/a', main.theme_get_audio),
]
