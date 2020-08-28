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
    cover = db.Column(db.String(), default="")
    year = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String())

    @classmethod
    def create(cls, title, mal_id, cover, year, season):
        anime = Anime(title=title, mal_id=mal_id, cover=cover, year=year, season=season)
        return anime.save()

    def save(self):
        row = Anime.query.filter_by(mal_id=self.mal_id).first()
        if not row:
            db.session.add(self)
            db.session.commit()
            return self, True
        else:
            db.session.commit()
            return self, False

    def json(self):
        theme_list = [theme.json() for theme in Theme.query.filter_by(mal_id=self.mal_id).all()]
        theme_list = sorted(theme_list, key=itemgetter('theme_id'), reverse=False)
        return {
            'mal_id': self.mal_id,
            'title': self.title[0],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': theme_list
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

    id = db.Column(db.Integer, primary_key=True)
    mal_id = db.Column(db.Integer, nullable=False)
    theme_id = db.Column(db.String(), nullable=False, unique=True)
    artist_id = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String())
    episodes = db.Column(db.String())
    category = db.Column(db.String())
    views = db.Column(db.Integer, default=0)
    mirrors = db.Column(JSONB)

    @classmethod
    def create(cls, title, type, mal_id, theme_id, notes, mirrors, episodes, category):
        theme = Theme(title=title, type=type, mal_id=mal_id, theme_id=theme_id, notes=notes,
                      mirrors=mirrors, category=category, episodes=episodes)
        # return theme.save()

    def update_or_create(mal_id, theme_id, title, type, notes, episodes, category, mirrors):
        theme = db.session.query(Theme).filter_by(theme_id=theme_id).first()
        if not theme:
            theme = Theme(title=title, type=type, mal_id=mal_id, theme_id=theme_id, notes=notes,
                          mirrors=mirrors, category=category, episodes=episodes)
            db.session.add(theme)
            db.session.commit()
            return theme, True
        else:
            theme.mirrors = mirrors
            theme.episodes = episodes
            db.session.commit()
            return theme, False

    def save(self):
        row = Theme.query.filter_by(theme_id=self.theme_id).first()
        if not row:
            db.session.add(self)
            db.session.commit()
            return self, True
        else:
            row.mirrors = self.mirrors
            row.episodes = self.episodes
            db.session.commit()
            return self, False

    def json(self):
        mirror_list = []
        for index, mirror in enumerate(self.mirrors):
            mirror['audio'] = f"{base_url}/{self.mal_id}/{self.theme_id.split('-')[1]}/{index}/audio"
            mirror_list.append(mirror)
        artist = Artist.query.filter_by(mal_id=self.artist_id).first()
        return {
            'theme_id': self.theme_id,
            'title': self.title,
            'type': self.type,
            'notes': self.notes,
            'artist': artist.name if artist else None,
            'mirrors': self.mirrors
        }

    def json_info(self):
        mirror_list = []
        for index, mirror in enumerate(self.mirrors):
            mirror['audio'] = f"{base_url}/{self.mal_id}/{self.theme_id.split('-')[1]}/{index}/audio"
            mirror_list.append(mirror)
        anime = Anime.query.filter_by(mal_id=self.mal_id).first()
        artist = Artist.query.filter_by(mal_id=self.artist_id).first()
        return {
            'theme_id': self.theme_id,
            'anime': anime.title[0],
            'mal_id': self.mal_id,
            'cover': anime.cover,
            'title': self.title,
            'type': self.type,
            'notes': self.notes,
            'artist': artist.name if artist else None,
            'mirrors': self.mirrors
        }

    def json_info_extended(self):
        anime = Anime.query.filter_by(mal_id=self.mal_id).first()
        return {
            'mal_id': self.mal_id,
            'title': anime.title[0],
            'cover': anime.cover,
            'year': anime.year,
            'season': anime.season,
            'themes': [self.json()]
        }

    def app_top_json(self):
        anime = Anime.query.filter_by(mal_id=self.mal_id).first()
        return {
            # THEME INFO
            'theme_id': self.theme_id,
            'title': self.title,
            'type': self.type,
            'views': self.views,
            # ANIME INFO
            'mal_id': self.mal_id,
            'name': anime.title[0],
            'cover': anime.cover,
        }

    def update(self):
        self.save()


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

    def json(self):
        theme_list = [Theme.query.filter_by(theme_id=item).first().json() for item in self.themes]
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
            'themes': theme_list
        }

    def app_detail_json(self):
        art_list = self.themes
        anime_list = []
        theme_ids = []
        for theme_id in art_list:
            mal_id = int(theme_id.split('-')[0])
            theme_ids.append(mal_id)
        theme_ids = list(dict.fromkeys(theme_ids))
        for mal_id in theme_ids:
            anime = Anime.query.filter_by(mal_id=mal_id).first()
            theme_entries = Theme.query.filter_by(mal_id=mal_id).all()
            theme_list = []
            for theme in theme_entries:
                if theme.theme_id in art_list:
                    theme_list.append(theme.json())
            anime_list.append(anime.artist_json(theme_list))
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
            'cover': self.cover
        }

    def update(self):
        self.save()
