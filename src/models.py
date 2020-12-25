import copy
import dataclasses
import json
from dataclasses import dataclass
from typing import Any

from src.helpers.picture import get_anime_picture, get_artist_picture

base = 'http://animethemes-api.herokuapp.com/api/v1/theme'


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
        return {'mal_id': self.anime_id, 'title': self.title.split(' | '), 'cover': self.cover, 'year': int(self.year),
                'season': self.season, 'themes': tmp_list}

    def app(self, extended=False):
        if extended:
            tmp_list = []
            from src.data.repo import theme_list
            for theme in theme_list:
                for theme_id in self.themes:
                    if theme_id == theme.theme_id:
                        tmp_list.append(theme.parse())
            return {'mal_id': self.anime_id, 'title': self.title.split(' | ')[0],
                    'cover': self.cover,
                    'year': int(self.year),
                    'season': self.season, 'themes': tmp_list}
        else:
            return {'mal_id': self.anime_id, 'title': self.title.split(' | ')[0], 'cover': self.cover,
                    'year': int(self.year),
                    'season': self.season}

    def __copy__(self):
        new = Anime(self.anime_id, self.title, self.cover, self.year, self.season, self.themes)
        return new

    def __eq__(self, other):
        return self.anime_id == other.anime_id


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

    def parse(self, extended=False):
        from src.data.repo import artist_list
        from src.data.repo import anime_list
        mirror_list = []
        for index, mirror in enumerate(self.mirrors):
            mirror['audio'] = f'{base}/{self.theme_id}/{index}/audio'
            mirror_list.append(mirror)
        if extended:
            anime = next((item for item in anime_list if item.anime_id == self.anime_id), None)
            return {'title': self.title, 'name': anime.title, 'cover': anime.cover, 'theme_id': self.theme_id,
                    'type': self.type,
                    'artist': next((item.name for item in artist_list if item.artist_id == self.artist_id), None),
                    'mirrors': mirror_list, 'notes': self.notes if self.notes else None, 'episodes': self.episodes,
                    'category': self.category if self.category else None}
        else:
            return {'title': self.title, 'theme_id': self.theme_id, 'type': self.type,
                    'artist': next((item.name for item in artist_list if item.artist_id == self.artist_id), None),
                    'mirrors': mirror_list, 'notes': self.notes if self.notes else None, 'episodes': self.episodes,
                    'category': self.category if self.category else None}

    def __eq__(self, other):
        if self.theme_id != other.theme_id:
            return False
        return True


@dataclass
class Artist:
    artist_id: int
    name: str
    cover: str
    themes: list

    __type__: str = 'Artist'

    def parse(self):
        themes = {}
        for theme_id in self.themes:
            mal_id = int(theme_id.split('-')[0])
            if not themes.get(mal_id):
                themes[mal_id] = []
            themes[mal_id].append(theme_id.split('-')[1])
        anime_list = []
        for mal_id, theme_ids in themes.items():
            from src.data.repo import anime_list as anime_list_repo
            anime = next((item.parse() for item in anime_list_repo if item.anime_id == mal_id), None)
            anime['title'] = anime['title'][0]
            theme_list = []
            for theme_id in theme_ids:
                theme_list.append(anime['themes'][int(theme_id)])
            anime['themes'] = theme_list
            anime_list.append(anime)
        return {'artist_id': self.artist_id, 'name': self.name,
                'cover': self.cover, 'themes': anime_list}

    def app(self):
        return {'artist_id': self.artist_id, 'name': self.name,
                'cover': self.cover}

    def __eq__(self, other):
        if self.artist_id != other.artist_id:
            return False
        return True
