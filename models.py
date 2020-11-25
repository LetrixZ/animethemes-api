from dataclasses import dataclass
from typing import Any


@dataclass
class Anime:
    anime_id: int
    title: str
    cover: Any
    year: int
    season: str
    themes: list


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


@dataclass
class Artist:
    artist_id: int
    name: str
    cover: str
    themes: list
