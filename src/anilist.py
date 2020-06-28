import requests

query = '''
query userList($user: String) {
  MediaListCollection(userName: $user, type: ANIME) {
    lists {
        entries {
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

def getListFromUser(user):
    variables = {
        'user': user
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    entries = response.json()['data']['MediaListCollection']['lists']
    aniList = []
    for entry in entries:
        aniList.extend(entry['entries'])
    return aniList

"""
dict = {
  "data": {
    "MediaListCollection": {
      "lists": [
        {
          "entries": [
            {
              "media": {
                "idMal": 38408
              }
            }
          ]
        },
        {
          "entries": [
            {
              "media": {
                "idMal": 38668
              }
            },
            {
              "media": {
                "idMal": 32827
              }
            },
            {
              "media": {
                "idMal": 36649
              }
            },
            {
              "media": {
                "idMal": 39195
              }
            },
            {
              "media": {
                "idMal": 39221
              }
            },
            {
              "media": {
                "idMal": 31043
              }
            },
            {
              "media": {
                "idMal": 31964
              }
            },
            {
              "media": {
                "idMal": 33486
              }
            },
            {
              "media": {
                "idMal": 36456
              }
            },
            {
              "media": {
                "idMal": 38656
              }
            },
            {
              "media": {
                "idMal": 1535
              }
            },
            {
              "media": {
                "idMal": 28223
              }
            },
            {
              "media": {
                "idMal": 35120
              }
            },
            {
              "media": {
                "idMal": 38691
              }
            },
            {
              "media": {
                "idMal": 32901
              }
            },
            {
              "media": {
                "idMal": 121
              }
            },
            {
              "media": {
                "idMal": 5114
              }
            },
            {
              "media": {
                "idMal": 270
              }
            },
            {
              "media": {
                "idMal": 34933
              }
            },
            {
              "media": {
                "idMal": 37086
              }
            },
            {
              "media": {
                "idMal": 38000
              }
            },
            {
              "media": {
                "idMal": 22535
              }
            },
            {
              "media": {
                "idMal": 28623
              }
            },
            {
              "media": {
                "idMal": 34544
              }
            },
            {
              "media": {
                "idMal": 23755
              }
            },
            {
              "media": {
                "idMal": 34577
              }
            },
            {
              "media": {
                "idMal": 31722
              }
            },
            {
              "media": {
                "idMal": 19815
              }
            },
            {
              "media": {
                "idMal": 20507
              }
            },
            {
              "media": {
                "idMal": 30276
              }
            },
            {
              "media": {
                "idMal": 13601
              }
            },
            {
              "media": {
                "idMal": 23281
              }
            },
            {
              "media": {
                "idMal": 16498
              }
            },
            {
              "media": {
                "idMal": 35760
              }
            },
            {
              "media": {
                "idMal": 22319
              }
            },
            {
              "media": {
                "idMal": 27899
              }
            },
            {
              "media": {
                "idMal": 36511
              }
            },
            {
              "media": {
                "idMal": 37521
              }
            },
            {
              "media": {
                "idMal": 33352
              }
            },
            {
              "media": {
                "idMal": 25777
              }
            },
            {
              "media": {
                "idMal": 37779
              }
            },
            {
              "media": {
                "idMal": 30503
              }
            },
            {
              "media": {
                "idMal": 323
              }
            },
            {
              "media": {
                "idMal": 37095
              }
            },
            {
              "media": {
                "idMal": 40060
              }
            },
            {
              "media": {
                "idMal": 39792
              }
            },
            {
              "media": {
                "idMal": 24833
              }
            },
            {
              "media": {
                "idMal": 30654
              }
            },
            {
              "media": {
                "idMal": 226
              }
            },
            {
              "media": {
                "idMal": 59
              }
            },
            {
              "media": {
                "idMal": 35928
              }
            },
            {
              "media": {
                "idMal": 6880
              }
            },
            {
              "media": {
                "idMal": 10418
              }
            },
            {
              "media": {
                "idMal": 39198
              }
            },
            {
              "media": {
                "idMal": 37520
              }
            },
            {
              "media": {
                "idMal": 40010
              }
            }
          ]
        },
        {
          "entries": [
            {
              "media": {
                "idMal": 11061
              }
            },
            {
              "media": {
                "idMal": 16033
              }
            },
            {
              "media": {
                "idMal": 32281
              }
            },
            {
              "media": {
                "idMal": 39701
              }
            },
            {
              "media": {
                "idMal": 31378
              }
            },
            {
              "media": {
                "idMal": 39491
              }
            },
            {
              "media": {
                "idMal": 11757
              }
            },
            {
              "media": {
                "idMal": 34902
              }
            },
            {
              "media": {
                "idMal": 35180
              }
            },
            {
              "media": {
                "idMal": 9253
              }
            },
            {
              "media": {
                "idMal": 39017
              }
            },
            {
              "media": {
                "idMal": 39196
              }
            },
            {
              "media": {
                "idMal": 37999
              }
            },
            {
              "media": {
                "idMal": 34134
              }
            },
            {
              "media": {
                "idMal": 32182
              }
            },
            {
              "media": {
                "idMal": 11617
              }
            },
            {
              "media": {
                "idMal": 24703
              }
            },
            {
              "media": {
                "idMal": 15451
              }
            },
            {
              "media": {
                "idMal": 34281
              }
            },
            {
              "media": {
                "idMal": 25157
              }
            },
            {
              "media": {
                "idMal": 30
              }
            },
            {
              "media": {
                "idMal": 777
              }
            },
            {
              "media": {
                "idMal": 38735
              }
            },
            {
              "media": {
                "idMal": 41120
              }
            },
            {
              "media": {
                "idMal": 23283
              }
            },
            {
              "media": {
                "idMal": 37987
              }
            },
            {
              "media": {
                "idMal": 14227
              }
            },
            {
              "media": {
                "idMal": 934
              }
            },
            {
              "media": {
                "idMal": 1889
              }
            },
            {
              "media": {
                "idMal": 3652
              }
            },
            {
              "media": {
                "idMal": 10491
              }
            },
            {
              "media": {
                "idMal": 36296
              }
            },
            {
              "media": {
                "idMal": 28405
              }
            },
            {
              "media": {
                "idMal": 33513
              }
            },
            {
              "media": {
                "idMal": 31716
              }
            },
            {
              "media": {
                "idMal": 40858
              }
            },
            {
              "media": {
                "idMal": 37497
              }
            },
            {
              "media": {
                "idMal": 30831
              }
            },
            {
              "media": {
                "idMal": 32937
              }
            },
            {
              "media": {
                "idMal": 38040
              }
            },
            {
              "media": {
                "idMal": 32380
              }
            },
            {
              "media": {
                "idMal": 34626
              }
            },
            {
              "media": {
                "idMal": 35241
              }
            },
            {
              "media": {
                "idMal": 39199
              }
            },
            {
              "media": {
                "idMal": 1482
              }
            },
            {
              "media": {
                "idMal": 8460
              }
            },
            {
              "media": {
                "idMal": 45
              }
            },
            {
              "media": {
                "idMal": 1818
              }
            },
            {
              "media": {
                "idMal": 33
              }
            },
            {
              "media": {
                "idMal": 6546
              }
            },
            {
              "media": {
                "idMal": 10620
              }
            },
            {
              "media": {
                "idMal": 32615
              }
            },
            {
              "media": {
                "idMal": 31405
              }
            },
            {
              "media": {
                "idMal": 33241
              }
            },
            {
              "media": {
                "idMal": 40591
              }
            },
            {
              "media": {
                "idMal": 39710
              }
            },
            {
              "media": {
                "idMal": 23273
              }
            },
            {
              "media": {
                "idMal": 28851
              }
            },
            {
              "media": {
                "idMal": 18679
              }
            },
            {
              "media": {
                "idMal": 9919
              }
            },
            {
              "media": {
                "idMal": 1
              }
            },
            {
              "media": {
                "idMal": 28121
              }
            },
            {
              "media": {
                "idMal": 199
              }
            },
            {
              "media": {
                "idMal": 15809
              }
            },
            {
              "media": {
                "idMal": 10087
              }
            },
            {
              "media": {
                "idMal": 11111
              }
            },
            {
              "media": {
                "idMal": 38671
              }
            },
            {
              "media": {
                "idMal": 34572
              }
            },
            {
              "media": {
                "idMal": 29803
              }
            },
            {
              "media": {
                "idMal": 38753
              }
            },
            {
              "media": {
                "idMal": 34822
              }
            },
            {
              "media": {
                "idMal": 6211
              }
            },
            {
              "media": {
                "idMal": 9989
              }
            },
            {
              "media": {
                "idMal": 15039
              }
            },
            {
              "media": {
                "idMal": 918
              }
            },
            {
              "media": {
                "idMal": 9969
              }
            },
            {
              "media": {
                "idMal": 28977
              }
            },
            {
              "media": {
                "idMal": 15417
              }
            },
            {
              "media": {
                "idMal": 34096
              }
            },
            {
              "media": {
                "idMal": 37451
              }
            },
            {
              "media": {
                "idMal": 16592
              }
            },
            {
              "media": {
                "idMal": 37435
              }
            },
            {
              "media": {
                "idMal": 39531
              }
            },
            {
              "media": {
                "idMal": 30885
              }
            },
            {
              "media": {
                "idMal": 31478
              }
            },
            {
              "media": {
                "idMal": 32867
              }
            },
            {
              "media": {
                "idMal": 38003
              }
            },
            {
              "media": {
                "idMal": 35062
              }
            },
            {
              "media": {
                "idMal": 3588
              }
            }
          ]
        },
        {
          "entries": [
            {
              "media": {
                "idMal": 40221
              }
            },
            {
              "media": {
                "idMal": 39463
              }
            }
          ]
        }
      ]
    }
  }
}

print(dict['data']['MediaListCollection']['lists'][0])
animeList = []
for entry in dict['data']['MediaListCollection']['lists']:
    animeList.extend(entry['entries'])
    print(entry)
print(len(animeList))"""