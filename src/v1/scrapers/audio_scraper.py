import concurrent.futures
import json
from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup


def get_bodies(url_list):
    def load_url(url, timeout):
        return requests.get(url, timeout=timeout)

    bodies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(load_url, url, 30): url for url in url_list}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            data = future.result()
            if len(data.content) > 2:
                bodies.append(data.content)
    return bodies


def get_request(name, page):
    name = name.replace("'", "")
    print(name)

    def get_body(name, page):
        page = requests.get("https://osanime.com/site-search.html?to-search={}&to-page={}".format(name, page)).content
        body = BeautifulSoup(page, 'html.parser')
        return body

    main = []
    response = get_body(name, page).find('main').findAll('img')
    print(len(main))
    while response:
        print(page)
        main += response
        page += 1
        response = get_body(name, page).find('main').findAll('img')
    return main


def get_audio(name, anime):
    body = get_request(name, 0)
    audio_list = []
    main = body.find('main').findAll('img')
    for entry in main:
        text = entry.get('alt').split(' - ')
        artist = text[0]
        title = text[1]
        text = entry.get('src').split('/')
        mirror = "{}//{}/ddl/{}/{}/audio.mp3".format(text[0], text[2], text[4], text[5])
        try:
            text = entry.parent.parent.find('a').text.split('[', 1)[1].split(']')[0].split(' ')
        except IndexError:
            print("name {}, artist: {}, title: {}".format(name, artist, title))
        if text[1].isnumeric():
            type = text[0] + " " + text[1]
            anime = ' '.join(text[2:])
        else:
            type = text[0]
            anime = ' '.join(text[1:])
        audio_list.append({'artist': artist, 'title': title, 'anime': anime, 'type': type, 'mirror': mirror})
    return audio_list


def get_audio_name(theme, anime):
    anime_name = json.loads(anime.title)[0]
    body = get_request(anime_name, 0)
    # main = body.find('main').findAll('img')
    print(theme.get('title') + " " + str(len(body)))
    for entry in body:
        text = entry.get('alt').split(' - ')
        artist = text[0]
        title = text[1]
        if SequenceMatcher(a=title, b=theme.get('title')).ratio() < 0.5:
            continue
        text = entry.get('src').split('/')
        mirror = "{}//{}/ddl/{}/{}/audio.mp3".format(text[0], text[2], text[4], text[5])
        return {'artist': artist, 'title': title, 'mirror': mirror}
    return None


def get_audio_anime(anime):
    anime_name = json.loads(anime.title)[0]
    main = get_request(anime_name, 0)
    themes = json.loads(anime.themes)
    added = []
    for entry in main:
        s = entry.get('alt').split(' - ')
        artist = s[0]
        title = s[1]
        for theme in themes:
            theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
            if SequenceMatcher(a=title, b=theme.get('title')).ratio() > 0.8:
                text = entry.get('src').split('/')
                mirror = "{}//{}/ddl/{}/{}/audio.mp3".format(text[0], text[2], text[4], text[5])
                theme['audio'] = {'artist': artist, 'title': title, 'mirror': mirror}
                added.append({'artist': artist, 'title': title, 'mirror': mirror})
                print("{} - {} ({})".format(artist, title, anime_name))
                break
    if not added:
        for theme in themes:
            theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
    return themes


def get_music(anime, name=None):
    anime_name = json.loads(anime.title)[0].lower()
    if name:
        anime_name = name
    body = get_request(anime_name, 0)
    themes = json.loads(anime.themes)
    # for entry in body:
    #     s = entry.get('alt').split(' - ')
    #     artist = s[0]
    #     title = s[1]
    #     info = entry.parent.parent.find('a').text.split('[', 1)[1].split(']')[0].lower()
    #     if SequenceMatcher(a=anime_name, b=info).ratio() > .4:
    #         for theme in themes:
    #             theme_title = theme.get('title')
    #             print(theme_title)
    #             if SequenceMatcher(a=theme_title, b=title).ratio() > .5:
    #                 print("{} found ({})".format(theme_title, anime_name))
    #                 text = entry.get('src').split('/')
    #                 mirror = "{}//{}/ddl/{}/{}/audio.mp3".format(text[0], text[2], text[4], text[5])
    #                 theme['audio'] = {'artist': artist, 'title': title, 'mirror': mirror}
    #                 break
    #             else:
    #                 print("{} NOT found ({})".format(theme_title, anime_name))
    #                 theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
    for theme in themes:
        try:
            if not theme.get('audio').get('mirror'):
                theme_title = theme.get('title')
                # print(theme_title)
                for entry in body:
                    # info = entry.parent.parent.find('a').text.split('[', 1)[1].split(']')[0].lower()
                    info = entry.parent.parent.find('a').text
                    info = info[info.find("[") + 1:info.find("]")]
                    if SequenceMatcher(a=anime_name.lower(), b=info.lower()).ratio() > .2:
                        s = entry.get('alt').split(' - ')
                        artist = s[0]
                        title = s[1]
                        if SequenceMatcher(a=theme_title.lower(), b=title.lower()).ratio() > .7:
                            print("{} = {} found ({})".format(theme_title, title, anime_name))
                            text = entry.get('src').split('/')
                            mirror = "{}//{}/ddl/{}/{}/audio.mp3".format(text[0], text[2], text[4], text[5])
                            theme['audio'] = {'artist': artist, 'title': title, 'mirror': mirror}
                            break
                        else:
                            # print("{} NOT found ({})".format(theme_title, anime_name))
                            theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
        except AttributeError:
            if not theme.get('audio'):
                theme_title = theme.get('title')
                # print(theme_title)
                for entry in body:
                    # info = entry.parent.parent.find('a').text.split('[', 1)[1].split(']')[0].lower()
                    info = entry.parent.parent.find('a').text
                    info = info[info.find("[") + 1:info.find("]")]
                    if SequenceMatcher(a=anime_name.lower(), b=info.lower()).ratio() > .2:
                        s = entry.get('alt').split(' - ')
                        artist = s[0]
                        title = s[1]
                        if SequenceMatcher(a=theme_title.lower(), b=title.lower()).ratio() > .7:
                            print("{} = {} found ({})".format(theme_title, title, anime_name))
                            text = entry.get('src').split('/')
                            mirror = "{}//{}/ddl/{}/{}/audio.mp3".format(text[0], text[2], text[4], text[5])
                            theme['audio'] = {'artist': artist, 'title': title, 'mirror': mirror}
                            break
                        else:
                            # print("{} NOT found ({})".format(theme_title, anime_name))
                            theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
    for theme in themes:
        if not theme.get('audio'):
            theme["audio"] = {'artist': None, 'title': None, 'mirror': None}
    print(themes)
    return themes
