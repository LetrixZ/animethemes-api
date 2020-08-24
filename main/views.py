import json
from operator import itemgetter

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.safestring import SafeString

from api.models import Anime, Theme
from api.v2.helpers.common import get_top_theme_list, get_latest_list, get_current, get_latest_theme_list

ANIME_PER_PAGE = 9
THEME_PER_PAGE = 20


def index(request):
    context = {'is_query': False}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    if len(query) > 1:
        query_list = get_queryset(query)
        anime_list = []
        for anime in query_list[0]:
            anime_list.append(anime.json())
        context['anime_list'] = anime_list
        theme_list = []
        for theme in query_list[1]:
            theme_list.append(theme.json())
        context['theme_list'] = theme_list
        context['is_query'] = True
    else:
        entries = Anime.objects.all().order_by('-id')[:10]
        anime_list = []
        theme_list = []
        for anime in entries:
            anime_list.append(anime.json())

    # Pagination
    if query:
        page = request.GET.get('page', 1)
        anime_list_paginator = Paginator(anime_list, ANIME_PER_PAGE)
        try:
            anime_list = anime_list_paginator.page(page)
        except PageNotAnInteger:
            anime_list = anime_list_paginator.page(ANIME_PER_PAGE)
        except EmptyPage:
            anime_list = anime_list_paginator.page(
                anime_list_paginator.num_pages)

        theme_list_pagination = Paginator(theme_list, THEME_PER_PAGE)
        try:
            theme_list = theme_list_pagination.page(page)
        except PageNotAnInteger:
            theme_list = theme_list_pagination.page(THEME_PER_PAGE)
        except EmptyPage:
            theme_list = theme_list_pagination.page(
                theme_list_pagination.num_pages)
    context['anime_list'] = anime_list
    context['theme_list'] = theme_list

    context['lists'] = [get_year_list(), current_list(), top_theme(), latest_list(), latest_theme()]

    return render(request, "main/home.html", context)


def theme(request, mal_id=1, theme_index=0, mirror=0):
    context = {}

    if request.POST:
        print(request.POST.get('theme_id', 0))
        theme_index = request.POST.get('theme_id', 0)

    anime = Anime.objects.filter(mal_id=mal_id).first()
    context['anime'] = anime.json()
    theme_index = str(theme_index)
    if len(theme_index) == 1:
        theme_index = "0" + theme_index
    try:
        context['theme'] = Theme.objects.filter(
            theme_id=f'{mal_id}-{theme_index}').first().json()
        context['current'] = theme_index
        context['mirror_index'] = mirror
    except AttributeError:
        pass

    theme_list = []
    for theme in Theme.objects.filter(mal_id=mal_id).all():
        theme_list.append(theme.json())
    theme_list = sorted(theme_list, key=itemgetter('theme_id'), reverse=False)
    context['theme_list'] = theme_list
    try:
        context['current'] = theme_list.index(context['theme'])
    except KeyError:
        pass
    context['theme_list_json'] = SafeString(json.dumps(theme_list))

    return render(request, "main/anime.html", context)


def year(request, year):
    context = {'year': year}
    entries = Anime.objects.all().filter(year=year)
    anime_list = []
    for entry in entries:
        anime_list.append(entry.json())
    context['list'] = anime_list
    context['seasons'] = year_seasons(None, year)
    return render(request, "main/year_list.html", context)


def year_seasons(request, year):
    results = Anime.objects.all().filter(year=year)
    seasons = []
    for item in results:
        season_text = item.season[:-5]
        if season_text not in seasons and len(season_text):
            seasons.append(season_text)
        elif 'All' not in seasons and item.season == 'All':
            seasons.append("All")
    seasons_list = []
    for season in seasons:
        season_list = []
        for item in results:
            if item.season[:-5] == season:
                season_list.append(item.json())
            elif item.season == 'All':
                season_list.append(item.json())
        season_list = sorted(season_list, key=lambda k: k['title'][0])
        seasons_list.append({'season': season, 'animes': season_list})
    seasons_list = sorted(seasons_list, key=lambda k: k['season'])
    return seasons_list


def get_year_list():
    entries = Anime.objects.all()
    item_list = set()
    for item in entries:
        item_list.add(item.year)
    return {f'Year': sorted(list(item_list), reverse=True)}


def top_theme():
    return {'Top 15 Themes': get_top_theme_list()}


def latest_list():
    return {f'Latest 15 added': get_latest_list()}


def current_list():
    current = get_current()
    return {f'{current[1]} {current[2]}': current[0]}


def latest_theme():
    return {'Latest themes added': get_latest_theme_list()}


def search_anime(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        anime_list = Anime.objects.filter(
            Q(title__icontains=q)
        ).distinct()
    for anime in anime_list:
        queryset.append(anime)
    return set(queryset)


def search_theme(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        theme_list = Theme.objects.filter(
                Q(title__icontains=q)
        ).distinct()
    for theme in theme_list:
        queryset.append(theme)
    return set(queryset)


def get_queryset(query=None):
    return [search_anime(query), search_theme(query)]
