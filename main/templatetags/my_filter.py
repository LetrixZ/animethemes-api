import json

from django import template

from api.models import Anime

register = template.Library()


@register.filter
def replace_commas(string):
    return string.replace('-', '/')
    # return string.split('-')


@register.filter
def get_id(string, index):
    return string.split('-')[index]


@register.filter
def get_at(list, index):
    return list[index]


@register.filter
def get_value_by_name(dict, key):
    return dict[key]


@register.filter
def get_item(theme, index):
    return translate(theme['mirrors'][index]['quality'])


@register.filter
def translate(quality):
    return [q.replace('NC', 'No Credits')
                .replace('BD', 'Blu-Ray')
                .replace('Trans', 'Transition')
                .replace('Over', 'Voice-Over')
                .replace('', 'Default') for q in quality]


@register.filter
def get_key(dictionary, index):
    return list(dictionary.keys())[index]


@register.filter
def get_value(dictionary, index):
    return list(dictionary.values())[index]


@register.filter
def get_image(year):
    return f'year/{year}.webp'


@register.filter
def escape_single_quotes(string):
    # The two backslashes are interpreted as a single one
    # because the backslash is the escaping character.
    return string.replace("'", "\\'")


@register.filter
def get_theme_index(string):
    return string.split('-')[1]


@register.filter
def get_name(mal_id):
    return Anime.objects.filter(mal_id=mal_id).first().title[0]


@register.filter
def get_views(views):
    if views == 1:
        return f'{views} view'
    else:
        return f'{views} views'
