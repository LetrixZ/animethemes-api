from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class Anime(db.Model):
    __tablename__ = 'animes'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    malId = db.Column(db.Integer, nullable=False, unique=True)
    cover = db.Column(db.String())
    year = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String())
    themes = db.Column(db.String())

    @classmethod
    def create(cls, title, malId, cover, year, season, themes):
        anime = Anime(title=title, malId=malId, cover=cover, year=year, season=season, themes=themes)
        return anime.save()

    def save(self):
        row = Anime.query.filter_by(malId=self.malId).first()
        if not row:
            db.session.add(self)
        else:
            row.cover = self.cover
            row.season = self.season
            row.themes = self.themes
        db.session.commit()
        return self

    def json(self):
        return {
            'malId': self.malId,
            'title': json.loads(self.title),
            'cover': self.cover,
            'season': self.season,
            'year': self.year,
            'themes': json.loads(self.themes)
        }

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def update(self):
        self.save()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    playId = db.Column(db.String(), nullable=True)

    @classmethod
    def create(cls, username, password):
        user = User(username=username, password=password)
        return user.save()

    def save(self):
        row = User.query.filter_by(username=self.username).first()
        if not row:
            # No existe
            db.session.add(self)
        else:
            # Existe, actualizando campos
            row.playId = self.playId
        db.session.commit()
        return self

    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'playId': self.playId
        }

    def update(self):
        self.save()


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    playId = db.Column(db.String(), nullable=False, unique=True)
    actualPlaylist = db.Column(db.Integer, nullable=False)
    playlists = db.Column(db.String())

    @classmethod
    def create(cls, playId):
        playlist = Playlist(playId=playId, actualPlaylist=0, playlists=json.dumps([{"lastPlayed": 0, "name": "",
                                                                                    'playlistItems': [],
                                                                                    'playId': playId,
                                                                                    'audioPlaylist': {"lastPlayed": 0,
                                                                                                      'name': '',
                                                                                                      'playlistItems': [],
                                                                                                      'playId': playId}}]))
        return playlist.save()

    def save(self):
        row = Playlist.query.filter_by(playId=self.playId).first()
        if not row:
            # No existe
            db.session.add(self)
        else:
            # Existe, actualizando campos
            row.playlist = self.playlists
            row.actualPlaylist = self.actualPlaylist
        db.session.commit()
        return self

    def json(self):
        return {
            'playId': self.playId,
            'actual_pos': self.actualPlaylist,
            'collection': json.loads(self.playlists)
        }

    def update(self):
        self.save()


class Theme(db.Model):
    __tablename__ = 'themes'
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    mal_id = db.Column(db.Integer, nullable=False)
    theme_id = db.Column(db.String(), nullable=False, primary_key=True)
    notes = db.Column(db.String())
    views = db.Column(db.Integer)
    mirrors = db.Column(db.String(), nullable=False)

    @classmethod
    def create(cls, title, type, mal_id, theme_id, notes, views, mirrors):
        theme = Theme(title=title, type=type, mal_id=mal_id, theme_id=theme_id, notes=notes, views=views,
                      mirrors=mirrors)
        # return theme
        return theme.save()

    def save(self):
        row = Theme.query.filter_by(theme_id=self.theme_id).first()
        if not row:
            db.session.add(self)
            # return self
        else:
            row.mirrors = self.mirrors
            # return None
        db.session.commit()
        return self

    def json(self):
        return {
            'title': self.title,
            'type': self.type,
            'mal_id': self.mal_id,
            'theme_id': self.theme_id,
            'notes': self.notes,
            'views': self.views,
            'mirrors': json.loads(self.mirrors)
        }

    def single_json(self):
        anime = Anime.query.filter_by(malId=self.mal_id).first()
        return {
            'malId': anime.malId,
            'title': json.loads(anime.title),
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
                'mirrors': json.loads(self.mirrors)}]
        }

    def update(self):
        self.save()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False
