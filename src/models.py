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
        for theme_index, theme in enumerate(self.themes):
            mirror_list = []
            for mirror_index, mirror in enumerate(theme['mirrors']):
                mirror['audio'] = f"{base_url}/{self.mal_id}/{theme_index}/{mirror_index}/audio"
                mirror['quality'] = ', '.join(mirror['quality'])
                mirror_list.append(mirror)
            theme['mirrors'] = mirror_list
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
            mirror['quality'] = ', '.join(mirror['quality'])
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
        mirror = self.mirrors[0]
        mirror['audio'] = f"{base_url}/{self.mal_id}/{self.theme_id.split('-')[1]}/{0}/audio"
        mirror['quality'] = ', '.join(mirror['quality'])
        return {
            # THEME INFO
            'theme_id': self.theme_id,
            'title': self.title,
            'type': self.type,
            'views': self.views,
            'mirrors': [mirror],
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

    def get_artist_themes(self):
        theme_list = []
        for theme_id in self.themes:
            mal_id = int(theme_id.split("-")[0])
            anime = Anime.query.filter_by(mal_id=mal_id).first()
            theme = anime.themes[int(theme_id.split("-")[1])]
            theme['cover'] = anime.cover
            theme['anime'] = anime.title[0]
            theme_list.append(theme)
        return theme_list

    def json(self):
        return {
            'mal_id': self.mal_id,
            'name': self.name,
            'cover': self.cover,
            'themes': self.get_artist_themes()
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
            theme_entries = self.get_artist_themes()
            theme_list = []
            for index, theme in enumerate(theme_entries):
                if f'{mal_id}-{index:02d}' in art_list:
                    mirror_list = []
                    for mirror_index, mirror in enumerate(theme['mirrors']):
                        mirror['audio'] = f"{base_url}/{self.mal_id}/{index}/{mirror_index}/audio"
                        mirror['quality'] = ', '.join(mirror['quality'])
                        mirror_list.append(mirror)
                    theme['mirrors'] = mirror_list
                    theme_list.append(theme)
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
