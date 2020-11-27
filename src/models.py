import copy
import dataclasses
import json
from dataclasses import dataclass
from typing import Any


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def object_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Anime':
        return Anime(obj['anime_id'], obj['title'], obj['cover'], obj['year'], obj['season'], obj['themes'])
    elif '__type__' in obj and obj['__type__'] == 'Artist':
        return Artist(obj['artist_id'], obj['name'], obj['cover'], obj['themes'])
    elif '__type__' in obj and obj['__type__'] == 'Theme':
        return Theme(obj['anime_id'], obj['artist_id'], obj['theme_id'], obj['title'], obj['type'], obj['notes'],
                     obj['episodes'], obj['category'], obj['mirrors'])
    return obj


@dataclass
class Anime:
    anime_id: int
    title: str
    cover: Any
    year: int
    season: str
    themes: list

    __type__: str = 'Anime'

    def parse(self):
        tmp_list = []
        from src.data.repo import theme_list
        for theme in theme_list:
            for theme_id in self.themes:
                if theme_id == theme.theme_id:
                    tmp_list.append(theme.parse())
        return {'mal_id': self.anime_id, 'title': self.title.split(' | '), 'cover': self.cover[0], 'year': self.year,
                'season': self.season, 'themes': tmp_list}

    def app(self):
        return {'mal_id': self.anime_id, 'title': self.title.split(' | ')[0], 'cover': self.cover[0], 'year': self.year,
                'season': self.season}

    def __copy__(self):
        new = Anime(self.anime_id, self.title, self.cover, self.year, self.season, self.themes)
        return new


@dataclass
class Theme:
    anime_id: int
    artist_id: Any
    theme_id: str
    title: str
    type: str
    notes: str
    episodes: str
    category: str
    mirrors: list

    __type__: str = 'Theme'

    def parse(self):
        from src.data.repo import artist_list
        return {'title': self.title, 'theme_id': self.theme_id, 'type': self.type,
                'artist': next((item.name for item in artist_list if item.artist_id == self.artist_id), None),
                'mirrors': self.mirrors, 'notes': self.notes, 'episodes': self.episodes, 'category': self.category}


@dataclass
class Artist:
    artist_id: int
    name: str
    cover: str
    themes: list

    __type__: str = 'Artist'

    def parse(self):
        tmp_list = []
        from src.data.repo import theme_list
        for theme in theme_list:
            for theme_id in self.themes:
                if theme_id == theme.theme_id:
                    tmp_list.append(theme)
        return {'artist_id': self.artist_id, 'name': self.name,
                'cover': [item for item in self.cover if 'voiceactors' in item][0], 'themes': tmp_list}

    def app(self):
        return {'artist_id': self.artist_id, 'name': self.name,
                'cover': [item for item in self.cover if 'voiceactors' in item][0]}
