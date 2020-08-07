import json
import praw
from bs4 import BeautifulSoup
from models import Artist, Theme

reddit = praw.Reddit(client_id="mS1uQkjEv2vxhg",
                     client_secret="Vs9q60YyROx780avM7AqsVFzfYM",
                     user_agent="Letrix's AnimeThemes API")


def parse_themes(body):
    anime_list = body.findAll('h3')
    theme_list = []
    for anime in anime_list:
        mal_url = anime.find('a').get('href')
        if 'myanimelist' not in mal_url:
            continue
        mal_id = int("".join(filter(str.isdigit, mal_url)))
        print(mal_id)
        theme_entries = Theme.query.filter_by(mal_id=mal_id).all()
        wiki_themes = anime.nextSibling.nextSibling.findAll('tr')[1:]
        if not wiki_themes:
            wiki_themes = anime.nextSibling.nextSibling.nextSibling.nextSibling.findAll('tr')[1:]
        for theme in wiki_themes:
            theme_type = theme.find('td').getText().split('"')[0][:-1]
            if not theme_type:
                continue
            for entry in theme_entries:
                if entry.type in theme_type:
                    theme_list.append({'theme_title': entry.title, 'theme_id': entry.theme_id})
                    break
    return theme_list


def parse_artist(entry):
    name = entry.getText()
    print(name)
    wiki = entry.find('a').get('href').split('/')[4:]
    page = reddit.subreddit('AnimeThemes').wiki['/'.join(wiki)].content_html
    body = BeautifulSoup(page, 'html.parser')
    mal_url = body.find('h2').find('a').get('href')
    if 'myanimelist' not in mal_url:
        mal_id = None
    else:
        mal_id = body.find('h2').find('a').get('href').split('/')[-1]
        if not mal_id:
            mal_id = body.find('h2').find('a').get('href').split('/')[-2]
        mal_id = int("".join(filter(str.isdigit, mal_id)))
    Artist.create(mal_id, name, None, json.dumps(parse_themes(body)))
    return {'name': name, 'cover': None, 'themes': parse_themes(body)}


def get_artists_list():
    page = reddit.subreddit('AnimeThemes').wiki['artist'].content_html
    body = BeautifulSoup(page, 'html.parser')
    artist_entries = body.findAll('p')[1:]
    artist_list = []
    for artist in artist_entries:
        artist_list.append(parse_artist(artist))
    return artist_list
