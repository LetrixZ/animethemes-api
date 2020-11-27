import requests

filters = ['CURRENT', 'PLANNING', 'COMPLETED', 'DROPPED', 'PAUSED', 'REPEATING']

query = '''
query userList($user: String) {
  MediaListCollection(userName: $user, type: ANIME) {
    lists {
      entries {
        status
        media {
          idMal
          title {
            romaji
          }
        }
      }
    }
  }
}
'''


def get_anilist(user, filter=None):
    variables = {
        'user': user
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    entries = response.json()['data']['MediaListCollection']['lists']
    anime_list = {}
    for entry in entries:
        status = entry['entries'][0]['status']
        anime_list[status] = []
        for anime in entry['entries']:
            anime_list[status].append(anime)
    if filter:
        return anime_list.get(filter)
    else:
        user_list = []
        for status, a_list in anime_list.items():
            user_list.extend(a_list)
        return user_list
