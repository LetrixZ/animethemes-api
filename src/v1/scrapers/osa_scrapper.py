import requests, re
from bs4 import BeautifulSoup
from models import OsaSong

key = 'a0469f6f7c39845fa23fee0576909dc8'


def get_items(page=1):
    page = requests.get('https://osanime.com/page-lists/1/Ost%20Anime/tp/' + str(page) + '.html').content
    body = BeautifulSoup(page, 'html.parser').find('article')
    items = []
    for item in body.select('a > div'):
        items.append(item)
    return items


def parse_songs(page=1):
    songs = []
    for item in get_items(page):
        songs.append(get_info(item)[0].json())
    return songs


def get_info(item):
    cover = item.find('img').get('src')
    mirror = cover.split('/')[0:-1]
    mirror[3] = 'download'
    mirror.insert(-1, key)
    text = item.find('b').text
    # print(text)
    artist = text[:text.find('[')].split('-')[0].strip()
    title = ' '.join(text[:text.find('[')].split('-')[1:]).lstrip().strip()
    mirror = '/'.join(mirror) + '/' + text
    try:
        info = re.search(r'\[.*?]', text.replace(artist, '').replace(title, '')).group(0)[1:-1]
    except IndexError:
        info = ""
        print("Error: " + text)
    except AttributeError:
        info = ""
        print("Error: " + text)
    try:
        duration = item.find('div', {'class': 'a3a3a3'}).text.split(' | ')[1]
        if len(duration.split(':')) > 1:
            duration = int(duration.split(':')[0]) * 60 + int(duration.split(':')[1])
        else:
            duration = int(duration.split(':')[0])
    except ValueError:
        duration = -1
        print("Error: " + text)
    songid = item.find('a').get('href')
    songid = int(songid[songid.find('=') + 1:])
    return OsaSong.create(songid, title, artist, cover, duration, mirror, info)
