from flask import Blueprint, jsonify

from models import Anime, Artist, Theme, db, OsaSong
from v1.scrapers.artist_scraper import get_list as artist_scrape
from v1.scrapers.reddit_scraper import get_year
from v1.scrapers.restore_data import get_anime_covers, get_artists
from v1.scrapers.osa_scrapper import parse_songs

scrapers = Blueprint('scraper', __name__)


@scrapers.route('artist')
def scrape_artist():
    return jsonify(artist_scrape())


@scrapers.route('year/<string:year>')
def scrape_year(year):
    return jsonify(get_year(year))


@scrapers.route('year/all')
def scrape_all_years():
    years = ['60s', '70s', '80s', '90s', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
             '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    added = {}
    for year in years:
        added[year] = get_year(year)
    return jsonify(added)


# @scrapers.route('print_all')
# def print_all_animes():
#     entries = Anime.query.all()
#     anime_list = []
#     for anime in entries:
#         anime_list.append(anime.app_json())
#     return jsonify(anime_list)
#
#
# @scrapers.route('print_all_artist')
# def print_all_artists():
#     entries = Artist.query.all()
#     artist_list = []
#     for artist in entries:
#         artist_list.append(artist.app_json())
#     return jsonify(artist_list)
#
#
# @scrapers.route('restore_covers')
# def restore_covers():
#     return jsonify(get_anime_covers())
#
#
# @scrapers.route('restore_artists')
# def restore_artist():
#     return jsonify(get_artists())


@scrapers.route('assign_artist')
def assign_artist():
    artist_list = Artist.query.all()
    for artist in artist_list:
        for theme in artist.themes:
            item = Theme.query.filter_by(theme_id=theme).first()
            try:
                item.artist_id = artist.mal_id
                item.save()
            except:
                return jsonify(artist.name, theme)
    return jsonify({'message': 'done'})


@scrapers.route('osanime')
def parse_osa_multi():
    songs = []
    for i in range(269, 278):
        songs.append(parse_songs(i))
    return jsonify(songs)


@scrapers.route('osanime/<int:page>')
def parse_osa(page):
    return jsonify(parse_songs(page))


@scrapers.route('song/<int:songid>')
def get_song(songid):
    song = OsaSong.query.filter_by(song_id=songid).first()
    return jsonify(song.json())


@scrapers.route('match')
def match_songs():
    to_remove = ['Ending', 'Opening', 'Theme Song', 'Ost.', 'Insert Song']
    song_list = OsaSong.query.all()
    anime_list = Anime.query.all()
    for song in song_list:
        if song.info == '' or song.info is None:
            continue
        # else:
        # print(song.json())
        anime_name = ' '.join(i for i in song.info.split() if i not in to_remove).strip()
        for anime in anime_list:
            if len(anime_name) > 1 and anime_name.lower() in str(anime.title):
                print(song.json())
                return jsonify(anime.json())
