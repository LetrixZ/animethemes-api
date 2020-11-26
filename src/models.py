import dataclasses
import json
from dataclasses import dataclass
from typing import Any
from dataclasses_json import dataclass_json


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


@dataclass_json
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
                    tmp_list.append(theme)
        self.themes = tmp_list
        return self


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
        self.themes = tmp_list
        return self
