from operator import itemgetter

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

base_url = 'https://animethemes-api.herokuapp.com/api/v1/anime'


class Anime(db.Model):
    __tablename__ = 'api_anime'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mal_id = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(JSONB, nullable=False)
    cover = db.Column(db.String(), nullable=True, default="")
    year = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String())
    themes = db.Column(JSONB, nullable=False)

    @classmethod
    def create(cls, title, mal_id, cover, year, season, themes):
        anime = Anime(title=title, mal_id=mal_id, cover=cover, year=year, season=season, themes=themes)
        return anime.save()

    def save(self):
        row = Anime.query.filter_by(mal_id=self.mal_id).first()
        if not row:
            db.session.add(self)
            db.session.commit()
            return self, True
        else:
            row.themes = self.themes
            db.session.commit()
            return self, False

    def json(self):
        theme_list = []
        entries = Theme.query.filter_by(mal_id=self.mal_id).all()
        # print(self.mal_id, entries)
        for theme in entries:
            theme_list.append(theme.json())
        return {
            'mal_id': self.mal_id,
            'title': self.title[0],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': theme_list
        }

    def json_raw(self):
        return {
            'mal_id': self.mal_id,
            'title': self.title[0],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': self.themes
        }

    def app_json(self):
        return {
            'mal_id': self.mal_id,
            'title': self.title[0],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
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


class Theme(db.Model):
    __tablename__ = 'api_theme'

    # Primary Key: 1-2-3
    id = db.Column(db.Integer, primary_key=True)
    # MAL ID: 40060. Tied to anime entry
    mal_id = db.Column(db.Integer, nullable=False)
    # Theme ID: 40060-1. Unique
    theme_id = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String())
    episodes = db.Column(db.String())
    category = db.Column(db.String())
    mirrors = db.Column(JSONB)

    @classmethod
    def create(cls, mal_id, theme_id, title, type, notes, episodes, category, mirrors):
        theme = Theme(mal_id=mal_id, theme_id=theme_id, title=title, type=type, notes=notes, episodes=episodes,
                      category=category, mirrors=mirrors)
        return theme.save()

    def save(self):
        row = Theme.query.filter_by(theme_id=self.theme_id).first()
        if not row:
            db.session.add(self)
            db.session.commit()
            return self, True
        else:
            row.mirrors = self.mirrors
            db.session.commit()
            return self, False

    def update(self):
        self.save()

    def json(self):
        mirror_list = []
        for mirror_index, mirror in enumerate(self.mirrors):
            mirror['audio'] = f"{base_url}/{self.mal_id}/{self.theme_id.split('-')[1]}/{mirror_index}/audio"
            mirror['quality'] = ', '.join(mirror['quality'])
            mirror_list.append(mirror)
        return {
            'title': self.title,
            'theme_id': self.theme_id,
            'type': self.type,
            'mirrors': mirror_list,
            'notes': self.notes,
            'episodes': self.episodes,
            'category': self.category,
        }


class Artist(db.Model):
    __tablename__ = 'api_artist'

    id = db.Column(db.Integer, primary_key=True)
    mal_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    cover = db.Column(db.String(), nullable=True, default="")
    themes = db.Column(JSONB)

    @classmethod
    def create(cls, mal_id, name, cover, themes):
        artist = Artist(mal_id=mal_id, name=name, cover=cover, themes=themes)
        return artist.save()

    def save(self):
        row = Artist.query.filter_by(mal_id=self.mal_id).first()
        if not row:
            db.session.add(self)
            db.session.commit()
            return self, True
        else:
            row.themes = self.themes
            db.session.commit()
            return self, False

    def get_artist_themes(self):
        theme_list = []
        for theme_id in self.themes:
            mal_id = int(theme_id.split("-")[0])
            anime = Anime.query.filter_by(mal_id=mal_id).first()
            # theme = anime.themes[int(theme_id.split("-")[1])]
            theme = Theme.query.filter_by(theme_id=theme_id).first()
            # try:
            #     theme.cover = anime.cover
            # except TypeError:
            #     print(anime.title, anime.mal_id)
            #     print(theme)
            # theme['anime'] = anime.title[0]
            theme_list.append(theme.json())
        return theme_list

    def json(self):
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
            'themes': self.get_artist_themes()
        }

    def app_detail_json(self):
        themes = {}
        for theme_id in self.themes:
            mal_id = int(theme_id.split('-')[0])
            if not themes.get(mal_id):
                themes[mal_id] = []
            themes[mal_id].append(theme_id.split('-')[1])
        anime_list = []
        for mal_id, theme_ids in themes.items():
            anime = Anime.query.filter_by(mal_id=mal_id).first().json()
            theme_list = []
            for theme_id in theme_ids:
                theme_list.append(anime['themes'][int(theme_id)])
            anime['themes'] = theme_list
            anime_list.append(anime)
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
            'themes': anime_list
        }

    def app_json(self):
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
        }

    def update(self):
        self.save()


class OsaSong(db.Model):
    __tablename__ = 'api_osasong'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    artist = db.Column(db.String(), nullable=False)
    # anime = db.Column(db.String(), nullable=False, default="")
    info = db.Column(db.String(), nullable=False)
    cover = db.Column(db.String(), nullable=False, default="")
    duration = db.Column(db.Integer, nullable=False)
    mirror = db.Column(db.String(), nullable=False)

    @classmethod
    def create(cls, song_id, title, artist, cover, duration, mirror, info):
        osasong = OsaSong(song_id=song_id, title=title, artist=artist, cover=cover, duration=duration, mirror=mirror,
                          info=info)
        return osasong.save()

    def save(self):
        row = OsaSong.query.filter_by(song_id=self.song_id).first()
        if not row:
            db.session.add(self)
            db.session.commit()
            return self, True
        else:
            db.session.commit()
            row.duration = self.duration
            return self, False

    def json(self):
        return {
            'song_id': self.song_id,
            'title': self.title,
            'artist': self.artist,
            'info': self.info,
            'cover': self.cover,
            'duration': self.duration,
            'mirror': self.mirror
        }
