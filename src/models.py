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
