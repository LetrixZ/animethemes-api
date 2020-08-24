from django.contrib import admin

from api.models import Anime, Theme, Artist

# Register your models here.
admin.site.register(Anime)
admin.site.register(Theme)
admin.site.register(Artist)
