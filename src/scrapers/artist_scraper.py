import json
import os
import praw
import requests
from bs4 import BeautifulSoup

from models import Artist, object_decoder, EnhancedJSONEncoder
from scrapers.anime_themes_scraper import get_mal_id

reddit = praw.Reddit(client_id=os.getenv('PRAW_CLIENT_ID'),
                     client_secret=os.getenv('PRAW_CLIENT_SECRET'),
                     user_agent="Letrix's AnimeThemes API")

local_artist_list = json.load(open('src/data/artist.json', 'r', encoding="utf8"), object_hook=object_decoder)


def get_cover(mal_id):
    print(f'cover: {mal_id}')
    page = requests.get("https://myanimelist.net/people/{}".format(mal_id))
    body = BeautifulSoup(page.content, 'html.parser')
    try:
        cover = body.find('img', {'class': 'lazyload'}).get('data-src')
        return cover
    except AttributeError:
        return None


def parse_themes(body, theme_list_db):
    anime_list = body.findAll('h3')
    theme_list = []
    for anime in anime_list:
        mal_id = get_mal_id(anime.find('a').get('href'))
        theme_entries = [item for item in theme_list_db if mal_id == item.anime_id]
        wiki_themes = anime.nextSibling.nextSibling.findAll('tr')[1:]
        if not wiki_themes:
            wiki_themes = anime.nextSibling.nextSibling.nextSibling.nextSibling.findAll('tr')[1:]
        for theme in wiki_themes:
            theme_type = theme.find('td').text.split(' "')[0]
            if not theme_type:
                continue
            for theme in theme_entries:
                if theme_type == theme.type:
                    theme_list.append(theme.theme_id)
    return theme_list


def parse_artist(entry, theme_list_db):
    name = entry.getText()
    wiki = entry.find('a').get('href').split('/')[4:]
    page = reddit.subreddit('AnimeThemes').wiki['/'.join(wiki)].content_html
    body = BeautifulSoup(page, 'html.parser')
    mal_url = body.find('h2').find('a').get('href')
    if 'myanimelist' not in mal_url:
        mal_id = None
        print(mal_url)
    else:
        mal_id = body.find('h2').find('a').get('href').split('/')[-1]
        if not mal_id:
            mal_id = body.find('h2').find('a').get('href').split('/')[-2]
        mal_id = int("".join(filter(str.isdigit, mal_id)))
    if name == 'OxT':
        mal_id = 12596
    if name == 'Spira*Spica':
        mal_id = 51708
    return Artist(mal_id, name, None, parse_themes(body, theme_list_db))


def get_list(theme_list_db):
    page = reddit.subreddit('AnimeThemes').wiki['artist'].content_html
    body = BeautifulSoup(page, 'html.parser')
    artist_entries = body.findAll('p')[1:]
    artist_list = []
    for item in artist_entries:
        artist = parse_artist(item, theme_list_db)
        if artist:
            if artist not in local_artist_list:
                print(artist)
                artist_list.append(artist)
            else:
                db_artist = next((index for index, item in enumerate(local_artist_list) if
                                  item.artist_id == artist.artist_id), None)
                if db_artist and local_artist_list[db_artist].themes != artist.themes:
                    print(
                        f'Updating artist with index {db_artist}, artist_id = {artist.artist_id}, name = {artist.name}')
                    local_artist_list[db_artist] = artist
                    with open("src/data/artist.json", 'w') as f:
                        json.dump(local_artist_list, f, cls=EnhancedJSONEncoder)
    return artist_list
