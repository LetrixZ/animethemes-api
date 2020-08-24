from django.contrib import admin
from django.urls import path, include

from api.v2.urls import main
from api.views import api_index, stats
from main.views import year, index, theme

version = 'api/v2/'

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/', api_index, name='api-index'),
    path('api/stats', stats, name='api-stats'),
    path(f'{version}', include(main)),

    path('', index, name='search-app'),
    path('id/<int:mal_id>/', theme, name='theme-app'),
    path('id/<int:mal_id>/<int:theme_index>/<int:mirror>/', theme, name='theme-app'),
    path('year/<int:year>', year, name='year-app'),
    path('id/<int:mal_id>/', theme, name='theme-post'),
    path('id/<int:mal_id>/undefined', theme, name='theme-app'),

]
