from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class Anime(db.Model):
    __tablename__ = 'animes'

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
    name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    playlists = db.Column(db.String())

    @classmethod
    def create(cls, name, password):
        user = User(name=name, password=password)
        return user.save()

    def save(self):
        row = User.query.filter_by(name=self.name).first()
        if not row:
            db.session.add(self)
        else:
            row.playlists = self.playlists
        db.session.commit()
        return self

    def json(self):
        return {
            'name': self.name,
            'password': self.password
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


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    playId = db.Column(db.String(8), unique=True, nullable=False)
    currentItem = db.Column(db.String())
    items = db.Column(db.String())

    @classmethod
    def create(cls, playId):
        playlist = Playlist(playId=playId)
        return playlist.save()

    def save(self):
        row = Playlist.query.filter_by(playId=self.playId).first()
        if not row:
            db.session.add(self)
        else:
            row.items = self.items
        db.session.commit()
        return self

    def json(self):
        return json.loads(self.items)

    def update(self):
        self.save()
