from difflib import SequenceMatcher
from models import OsaSong, Anime, db
from flask import Blueprint, jsonify
from sqlalchemy.orm.attributes import flag_modified

music_app = Blueprint('music', __name__)


@music_app.route('/')
def index_music():
    return jsonify({'author': 'u/LetrixZ', 'version': 'v1',
                    'message': 'all data here is gathered from osanime.com; it\'s possible that you may encounter '
                               'some mismatches here; report all problems to u/LetrixZ on Reddit.',
                    'endpoints': [{
                        'id/<int:song_id>': 'get the song with the id of the osanime.com website',
                        'search/<path:name>': 'search in the database for music that matches that '
                                              'filter; it includes artist, title of the song and name '
                                              'of the anime.'}]})


@music_app.route('id/<int:song_id>')
def get_by_id(song_id):
    return jsonify(OsaSong.query.filter_by(song_id=song_id).first().json())


@music_app.route('search/<path:name>')
def search_music(name):
    # to_remove = ['Ending', 'Opening', 'Theme Song', 'Ost.', 'Insert Song']
    song_list = OsaSong.query.all()
    results = []
    for song in song_list:
        # anime_name = ' '.join(i for i in song.info.split() if i not in to_remove)
        anime_name = song.info \
            .replace('Theme Song', '') \
            .replace('Ending', '') \
            .replace('Opening', '') \
            .replace('Ost.', '') \
            .replace('Insert Song', '')
        if name.lower() in anime_name.lower() or name.lower() in song.artist.lower() or name.lower() in song.title.lower():
            results.append(song.json())
    l_set = set()
    new_list = []
    for dct in results:
        t = tuple(dct.items())
        if t not in l_set:
            l_set.add(t)
            new_list.append(dct)
    return jsonify(new_list)


# @music_app.route('db/test')
def test_match():
    # anime_list = Anime.query.all()
    # song_list = OsaSong.query.all()
    matches = []
    for song in OsaSong.query.all():
        for anime in Anime.query.all():
            for a_title in anime.title:
                if a_title.lower() in song.info.lower() and SequenceMatcher(a=song.info.lower(),
                                                                            b=a_title.lower()).ratio() > .6:
                    theme_list = anime.themes
                    for theme in theme_list:
                        if SequenceMatcher(a=theme['title'].lower(), b=song.title.lower()).ratio() > .6:
                            theme['song'] = song.mirror.strip()
                            matches.append({'song': '%s - %s' % (song.artist, song.title), 'anime': anime.title[0]})
                    flag_modified(anime, "themes")
                    db.session.add(anime)
                    db.session.commit()
                    # anime.themes = theme_list
                    # print(anime.themes)
                    # anime.save()
                    print(anime.themes)
                    break
            # anime.save()
    return jsonify(matches)
