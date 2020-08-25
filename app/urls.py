from django.contrib import admin
from django.urls import path, include

from api.v1.urls import main as main_v1
from api.v2.urls import main as main_v2
from api.views import api_index, stats
from main.views import year, home, theme

v1 = 'api/v1/'
v2 = 'api/v2/'

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/', api_index, name='api-index'),
    path('api/stats', stats, name='api-stats'),
    path(f'{v2}', include(main_v2)),
    path(f'{v1}', include(main_v1)),

    path('', home, name='search-app'),
    path('id/<int:mal_id>', theme, name='theme-app'),
    path('id/<int:mal_id>/<int:theme_index>/<int:mirror>/', theme, name='theme-app'),
    path('year/<int:year>', year, name='year-app'),
    path('id/<int:mal_id>/', theme, name='theme-post'),

]
