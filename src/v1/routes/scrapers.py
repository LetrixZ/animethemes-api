from flask import Blueprint, jsonify

from models import Artist, Theme, db
from v1.scrapers.artist_scraper import get_list as artist_scrape
from v1.scrapers.reddit_scraper import get_year
from v1.scrapers.restore_data import get_anime_covers, get_artists

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


@scrapers.route('restore_covers')
def restore_covers():
    return jsonify(get_anime_covers())


@scrapers.route('restore_artists')
def restore_artist():
    return jsonify(get_artists())


@scrapers.route('assign_artist')
def assign_artist():
    for artist in Artist.query.all():
        for theme in artist.themes:
            item = Theme.query.filter_by(theme_id=theme).first()
            try:
                item.artist_id = artist.mal_id
                item.save()
            except:
                return jsonify(artist.name, theme)
    # db.session.commit()
    return jsonify({'message': 'done'})

