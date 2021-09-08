import json
from db_models import Anime, Theme, Artist, db


def map_list(it):
    titles = it['title'].split(' | ')
    it['title'] = titles[0]
    it['synonyms'] = None
    if len(titles) > 1:
        it['synonyms'] = titles[1:]
    if 'All' in it['season']:
        it['season'] = 'UNKNOWN'
    return {'mal_id': it['anime_id'], 'title': it['title'], 'synonyms': it['synonyms'], 'cover': it['cover'], 'year': it['year'], 'season': it['season'], 'themes_id': it['themes']}


def process():
    anime_list = json.loads(open('src/data/anime.json', encoding='utf8').read())
    theme_list = json.loads(open('src/data/themes.json', encoding='utf8').read())
    anime_list_mapped = list(map(map_list, anime_list))
    for it in anime_list_mapped:
        row_anime = Anime(mal_id=it['mal_id'], title=it['title'], synonyms=it['synonyms'], cover=it['cover'], year=it['year'], season=it['season'])
        for theme in theme_list:
            if theme['anime_id'] == it['mal_id']:
                row_theme = Theme(title=theme['title'], slug=theme['theme_id'], type=theme['type'], notes=theme['notes'], episodes=theme['episodes'], category=theme['category'],
                      anime=row_anime, mirrors=theme['mirrors'])
                db.session.add(row_theme)
    artist_list = json.loads(open('src/data/artist.json', encoding='utf8').read())
    artist_list = [i for n, i in enumerate(artist_list) if i not in artist_list[n + 1:]]
    for artist in artist_list:
        row_artist = Artist(mal_id=artist['artist_id'], name=artist['name'], picture=artist['cover'])
        db.session.add(row_artist)
        for theme in artist['themes']:
            theme_row = Theme.query.filter_by(slug=theme).first()
            if theme_row:
                theme_row.artist_id = row_artist.id
                db.session.add(theme_row)
    db.session.commit()
