import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# ----- This is related code -----
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


class Anime(Base):
    __tablename__ = 'api_anime_test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mal_id = Column(Integer, nullable=False, unique=True)
    title = Column(String, nullable=False)
    cover = Column(String, nullable=True, default="")
    year = Column(Integer, nullable=False)
    season = Column(String)
    themes = Column(JSONB, nullable=False)

    @classmethod
    def create(cls, title, mal_id, cover, year, season, themes):
        anime = Anime(title=title, mal_id=mal_id, cover=cover, year=year, season=season, themes=themes)
        return anime.save()

    def save(self):
        # row = Anime.query.filter_by(mal_id=self.mal_id).first()
        row = session.query(Anime).filter_by(mal_id=self.mal_id).first()
        if not row:
            session.add(self)
            session.commit()
            return self, True
        else:
            row.themes = self.themes
            session.commit()
            return self, False

    def json(self):
        theme_list = []
        entries = session.query(Theme).filter_by(mal_id=self.mal_id).all()
        for theme in entries:
            theme_list.append(theme.json())
        return {
            'mal_id': self.mal_id,
            'title': self.title.split(' | ')[0],
            'synonyms': self.title.split(' | ')[1:],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': theme_list
        }

    def json_raw(self):
        return {
            'mal_id': self.mal_id,
            'title': self.title.split(' | ')[0],
            'synonyms': self.title.split(' | ')[1:],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': self.themes
        }

    def app_json(self):
        return {
            'mal_id': self.mal_id,
            'title': self.title.split(' | ')[0],
            'synonyms': self.title.split(' | ')[1:],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
        }

    def artist_json(self, theme_list):
        return {
            'mal_id': self.mal_id,
            'title': self.title.split(' | ')[0],
            'synonyms': self.title.split(' | ')[1:],
            'cover': self.cover,
            'year': self.year,
            'season': self.season,
            'themes': theme_list
        }


class Theme(Base):
    __tablename__ = 'api_theme_test'

    # Primary Key: 1-2-3
    id = Column(Integer, primary_key=True)
    # MAL ID: 40060. Tied to anime entry
    mal_id = Column(Integer, nullable=False)
    # Theme ID: 40060-1. Unique
    theme_id = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    notes = Column(String)
    episodes = Column(String)
    category = Column(String)
    mirrors = Column(JSONB)
    artist_id = Column(Integer, nullable=True)

    @classmethod
    def create(cls, mal_id, theme_id, title, type, notes, episodes, category, mirrors):
        theme = Theme(mal_id=mal_id, theme_id=theme_id, title=title, type=type, notes=notes, episodes=episodes,
                      category=category, mirrors=mirrors)
        return theme.save()

    def save(self):
        # row = Theme.query.filter_by(theme_id=self.theme_id).first()
        row = session.query(Theme).filter_by(theme_id=self.theme_id).first()
        if not row:
            session.add(self)
            session.commit()
            return self, True
        else:
            row.mirrors = self.mirrors
            session.commit()
            return self, False

    def update(self):
        self.save()

    def json(self):
        mirror_list = []
        artist = session.query(Artist).filter_by(mal_id=self.artist_id).first()
        for mirror_index, mirror in enumerate(self.mirrors):
            mirror['audio'] = f"{'base_url'}/{self.mal_id}/{self.theme_id.split('-')[1]}/{mirror_index}/audio"
            mirror['quality'] = ', '.join(mirror['quality'])
            mirror_list.append(mirror)
        return {
            'title': self.title,
            'theme_id': self.theme_id,
            'type': self.type,
            'artist': artist.name if artist is not None else '',
            'mirrors': mirror_list,
            'notes': self.notes,
            'episodes': self.episodes,
            'category': self.category,
        }


class Artist(Base):
    __tablename__ = 'api_artist_test'

    id = Column(Integer, primary_key=True)
    mal_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    cover = Column(String, nullable=True, default="")
    themes = Column(JSONB)

    @classmethod
    def create(cls, mal_id, name, cover, themes):
        artist = Artist(mal_id=mal_id, name=name, cover=cover, themes=themes)
        return artist.save()

    def save(self):
        row = session.query(Artist).filter_by(mal_id=self.mal_id).first()
        if not row:
            session.add(self)
            session.commit()
            return self, True
        else:
            row.themes = self.themes
            session.commit()
            return self, False

    def get_artist_themes(self):
        theme_list = []
        for theme_id in self.themes:
            mal_id = int(theme_id.split("-")[0])
            theme = session.query(Theme).filter_by(theme_id=theme_id).first()
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


Base.metadata.create_all(engine)
