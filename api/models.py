from operator import itemgetter

from django.db import models


class Anime(models.Model):
    id = models.AutoField(primary_key=True)
    mal_id = models.IntegerField(unique=True)
    title = models.JSONField()
    cover = models.TextField(default="")
    year = models.IntegerField()
    season = models.CharField(max_length=20)

    def json(self):
        theme_list = [theme.theme_json() for theme in Theme.objects.filter(mal_id=self.mal_id).all()]
        theme_list = sorted(theme_list, key=itemgetter('theme_id'), reverse=False)
        return {
            'mal_id': self.mal_id,
            'title': self.title[0],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': theme_list
        }

    def v1_json(self):
        theme_list = [theme.theme_json() for theme in Theme.objects.filter(mal_id=self.mal_id).all()]
        theme_list = sorted(theme_list, key=itemgetter('theme_id'), reverse=False)
        return {
            'malId': self.mal_id,
            'title': self.title,
            'cover': self.cover,
            'season': self.season,
            'year': self.year,
            'themes': theme_list
        }

    def artist_json(self, theme_list):
        return {
            'mal_id': self.mal_id,
            'title': self.title[0],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': theme_list
        }


class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    mal_id = models.IntegerField()
    theme_id = models.TextField(unique=True)
    artist_id = models.IntegerField(blank=True, default=-1)
    title = models.TextField()
    type = models.CharField(max_length=20)
    notes = models.TextField(blank=True, default="")
    category = models.TextField(blank=True, default="")
    episodes = models.TextField(blank=True, default="")
    views = models.IntegerField(default=0)
    mirrors = models.JSONField()

    def json(self):
        anime = Anime.objects.filter(mal_id=self.mal_id).first()
        mirror_list = []
        for index, mirror in enumerate(self.mirrors):
            mirror[
                'audio'] = f"https://animethemes-api.herokuapp.com/api/v1/anime/{self.mal_id}/{self.theme_id.split('-')[1]}/{index}/audio "
            mirror_list.append(mirror)
        return {
            'name': anime.title[0],
            'mal_id': self.mal_id,
            'theme_id': self.theme_id,
            'artist': Artist.objects.filter(mal_id=self.artist_id).first().name if Artist.objects.filter(
                mal_id=self.artist_id).first() else "",
            'title': self.title,
            'cover': anime.cover,
            'type': self.type,
            'notes': self.notes,
            'category': self.category,
            'episodes': self.episodes,
            'views': self.views,
            'mirrors': mirror_list
        }

    def theme_json(self):
        mirror_list = []
        for index, mirror in enumerate(self.mirrors):
            mirror[
                'audio'] = f"https://animethemes-api.herokuapp.com/api/v1/anime/{self.mal_id}/{self.theme_id.split('-')[1]}/{index}/audio "
            mirror_list.append(mirror)
        return {
            'mal_id': self.mal_id,
            'theme_id': self.theme_id,
            'artist': Artist.objects.filter(mal_id=self.artist_id).first().name if Artist.objects.filter(
                mal_id=self.artist_id).first() else "",
            'title': self.title,
            'type': self.type,
            'notes': self.notes,
            'category': self.category,
            'episodes': self.episodes,
            'views': self.views,
            'mirrors': mirror_list
        }

    def v1_json(self):
        mirrors = self.mirrors
        mirror_list = []
        for index, mirror in enumerate(mirrors):
            mirror[
                'audioUrl'] = f"https://animethemes-api.herokuapp.com/api/v1/anime/{self.mal_id}/{self.theme_id.split('-')[1]}/{index}/audio"
            mirror_list.append(mirror)
        return {
            'title': self.title,
            'type': self.type,
            'mal_id': self.mal_id,
            'theme_id': self.theme_id,
            'notes': self.notes,
            'views': self.views,
            'mirrors': mirror_list,
            # 'mirrors': json.loads(self.mirrors),
            'artist': Artist.objects.filter(mal_id=self.artist_id).first().name if Artist.objects.filter(
                mal_id=self.artist_id).first() else "",
        }

    def single_json(self):
        anime = Anime.objects.filter(mal_id=self.mal_id).first()
        return {
            'malId': anime.malId,
            'title': anime.title,
            'cover': anime.cover,
            'season': anime.season,
            'year': anime.year,
            'themes': [{
                'title': self.title,
                'type': self.type,
                'mal_id': self.mal_id,
                'theme_id': self.theme_id,
                'notes': self.notes,
                'views': self.views,
                'mirrors': self.mirrors}],
            'artist': Artist.objects.filter(mal_id=self.artist_id).first().name if Artist.objects.filter(
                mal_id=self.artist_id).first() else "",
        }


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    mal_id = models.IntegerField(unique=True)
    name = models.TextField()
    cover = models.TextField(default="")
    themes = models.JSONField()

    def json(self):
        art_list = self.themes
        anime_list = []
        theme_ids = []
        for theme_id in art_list:
            mal_id = int(theme_id.split('-')[0])
            theme_ids.append(mal_id)
        theme_ids = list(dict.fromkeys(theme_ids))
        for mal_id in theme_ids:
            anime = Anime.objects.filter(mal_id=mal_id).first()
            theme_entries = Theme.objects.filter(mal_id=mal_id).all()
            theme_list = []
            for theme in theme_entries:
                if theme.theme_id in art_list:
                    theme_list.append(theme.json())
            # anime_list.append(
            #     {'cover': anime.cover, 'mal_id': anime.mal_id, 'season': None, 'themes': theme_list,
            #      'title': json.loads(anime.title)[0], 'year': None})
            anime_list.append(anime.artist_json(theme_list))
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
            'themes': anime_list
        }

    def v1_json(self):
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
            'themes': self.themes
        }
