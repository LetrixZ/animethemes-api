## Update

AnimeThemes has an official API [https://staging.animethemes.moe/](https://staging.animethemes.moe/) and audio only mode is [planned](https://github.com/AnimeThemes/animethemes-server/issues/225).

I will keep updating this whenever I can. I'll probably end up switching to a proper database again and do automatic updates.

# AnimeThemes unofficial API

This an AnimeThemes API written in Python. It works by scraping data from the subreddit ([r/AnimeThemes](https://www.reddit.com/r/AnimeThemes/)) and saving it to different JSON files under 'data' folder. This is done by the scraping script that is present in the code.

The API is deployed in Heroku and is powered by Flask.

## End-points

### Get anime's info

/api/v1/anime/:anime_id

Returns info related to an anime that is identified by the 'anime_id' (MyAnimeList anime's ID).

Example output:

/api/v1/anime/40060

```json
{
  "mal_id": 40060,
  "title": ["BNA", "Brand New Animal"],
  "cover": "https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
  "year": 2020,
  "season": "Spring 2020",
  "themes": [
    {
      "title": "Ready to",
      "theme_id": "40060-00",
      "type": "OP V1",
      "artist": null,
      "mirrors": [
        {
          "quality": "",
          "mirror": "https://animethemes.moe/video/BrandNewAnimal-OP1.webm",
          "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/40060-00/0/audio"
        }
      ],
      "notes": "",
      "episodes": "1-5",
      "category": ""
    },
    {
      "title": "Ready to",
      "theme_id": "40060-01",
      "type": "OP V2",
      "artist": null,
      "mirrors": [
        {
          "quality": "",
          "mirror": "https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm",
          "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/40060-01/0/audio"
        }
      ],
      "notes": "",
      "episodes": "6-11",
      "category": ""
    },
    {
      "title": "NIGHT RUNNING",
      "theme_id": "40060-02",
      "type": "ED V1",
      "artist": null,
      "mirrors": [
        {
          "quality": "",
          "mirror": "https://animethemes.moe/video/BrandNewAnimal-ED1.webm",
          "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/40060-02/0/audio"
        }
      ],
      "notes": "",
      "episodes": "1-6",
      "category": ""
    },
    {
      "title": "NIGHT RUNNING",
      "theme_id": "40060-03",
      "type": "ED V2",
      "artist": null,
      "mirrors": [
        {
          "quality": "",
          "mirror": "https://animethemes.moe/video/BrandNewAnimal-ED1v2.webm",
          "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/40060-03/0/audio"
        }
      ],
      "notes": "",
      "episodes": "7-10",
      "category": ""
    },
    {
      "title": "NIGHT RUNNING",
      "theme_id": "40060-04",
      "type": "ED V3",
      "artist": null,
      "mirrors": [
        {
          "quality": "",
          "mirror": "https://animethemes.moe/video/BrandNewAnimal-ED1v3.webm",
          "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/40060-04/0/audio"
        }
      ],
      "notes": "",
      "episodes": "11",
      "category": ""
    }
  ]
}
```

### Get artist's info

/api/v1/artist/:artist_id

Returns info related to an artist that is identified by the 'artist_id' (MyAnimeList people's ID).

Example output (truncated):

/api/v1/artist/10561

```json
{
  "artist_id": 10561,
  "name": "LiSA",
  "cover": "https://cdn.myanimelist.net/images/voiceactors/2/36293.jpg",
  "themes": [
    {
      "mal_id": 6547,
      "title": "Angel Beats!",
      "cover": "https://cdn.myanimelist.net/images/anime/10/22061.jpg",
      "year": 2010,
      "season": "Spring 2010",
      "themes": [
        {
          "title": "My Soul, Your Beats!",
          "theme_id": "6547-01",
          "type": "OP2",
          "artist": "LiSA",
          "mirrors": [
            {
              "quality": "BD, 1080",
              "mirror": "https://animethemes.moe/video/AngelBeats-OP2.webm",
              "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/6547-01/0/audio"
            }
          ],
          "notes": "",
          "episodes": "4",
          "category": ""
        },
        {
          "title": "Ichiban no Takaramono ~Yui final ver.~",
          "theme_id": "6547-03",
          "type": "ED2",
          "artist": "LiSA",
          "mirrors": [
            {
              "quality": "Over",
              "mirror": "https://animethemes.moe/video/AngelBeats-ED2.webm",
              "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/6547-03/0/audio"
            }
          ],
          "notes": "Spoiler",
          "episodes": "10",
          "category": ""
        }
      ]
    }
  ]
}
```

### Get theme's info

/api/v1/theme/:theme_id

Returns info related to a theme that is identified by the 'theme_id' (format: 'anime_id'-index).

Example output:

/api/v1/theme/40060-00

```json
{
  "title": "Ready to",
  "theme_id": "40060-00",
  "type": "OP V1",
  "artist": null,
  "mirrors": [
    {
      "quality": "",
      "mirror": "https://animethemes.moe/video/BrandNewAnimal-OP1.webm",
      "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/40060-00/0/audio"
    }
  ],
  "notes": "",
  "episodes": "1-5",
  "category": ""
}
```

### Search content in the data base

/api/v1/search/:search

Returns a dict containing list of anime, artists and themes.

Example output (truncated):

/api/v1/search/night

```json
{
  "anime": [
    {
      "mal_id": 3024,
      "title": ["Ribbon no Kishi", "Princess Knight"],
      "cover": "https://cdn.myanimelist.net/images/anime/2/4403.jpg",
      "year": 60,
      "season": "All 60s",
      "themes": [
        {
          "title": "Ribbon No Kishi",
          "theme_id": "3024-00",
          "type": "OP",
          "artist": null,
          "mirrors": [
            {
              "quality": "DVD, 480",
              "mirror": "https://animethemes.moe/video/RibbonNoKishi-OP1.webm",
              "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/3024-00/0/audio"
            }
          ],
          "notes": "",
          "episodes": "",
          "category": ""
        },
        {
          "title": "Ribbon No March",
          "theme_id": "3024-01",
          "type": "ED",
          "artist": null,
          "mirrors": [
            {
              "quality": "DVD, 480",
              "mirror": "https://animethemes.moe/video/RibbonNoKishi-ED1.webm",
              "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/3024-01/0/audio"
            }
          ],
          "notes": "",
          "episodes": "",
          "category": ""
        }
      ]
    }
  ],
  "themes": [
    {
      "title": "Space Knights no Uta",
      "theme_id": "1458-01",
      "type": "ED",
      "artist": null,
      "mirrors": [
        {
          "quality": "480",
          "mirror": "https://animethemes.moe/video/UchuuNoKishiTekkaman-ED1.webm",
          "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/1458-01/0/audio"
        }
      ],
      "notes": "",
      "episodes": "",
      "category": ""
    }
  ],
  "artist": [
    {
      "artist_id": 6201,
      "name": "Nightmare",
      "cover": "https://cdn.myanimelist.net/images/voiceactors/1/44467.jpg",
      "themes": [
        {
          "mal_id": 1818,
          "title": "Claymore",
          "cover": "https://cdn.myanimelist.net/images/anime/3/21834.jpg",
          "year": 2007,
          "season": "Spring 2007",
          "themes": [
            {
              "title": "Raison D'être",
              "theme_id": "1818-00",
              "type": "OP",
              "artist": "Nightmare",
              "mirrors": [
                {
                  "quality": "NC, BD",
                  "mirror": "https://animethemes.moe/video/Claymore-OP1.webm",
                  "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/1818-00/0/audio"
                }
              ],
              "notes": "",
              "episodes": "",
              "category": ""
            }
          ]
        }
      ]
    }
  ]
}
```

/api/v1/search/anime/:search

Returns a dict containing list of anime.

/api/v1/search/artist/:search

Returns a dict containing list of artists.

/api/v1/search/theme/:search

Returns a dict containing list of themes.

### Get video mirror (redirect)

/api/v1/theme/:theme_id/video

/api/v1/theme/:theme_id/:quality/video

Redirects to the requested mirror of a theme identified by 'theme_id'. 'quality' is the index of the desired mirror for that quality. Check theme's info for a list of mirrors.

/api/v1/theme/35062-00/1/video

Example output:

Redirection to https://animethemes.moe/video/MahoutsukaiNoYome-OP1-Lyrics.webm

### Extract audio from video

/api/v1/theme/:theme_id/audio

/api/v1/theme/:theme_id/:quality/audio

Extracts the audio from the video file of the theme identified by 'theme_id' and uploads to ephemeral file system server (temporal storage). Then, it redirects to the download link.

### Get list of years, seasons, current season and all seasons

/api/v1/season/all

Return a list of all years with their available seasons.

Example output (truncated):

```json
{
  "2000": ["Winter", "Spring", "Summer", "Fall"],
  "2020": ["Winter", "Spring", "Summer", "Fall"]
}
```

/api/v1/season/years

Return a list of all years available.

Example output:

```json
[
  60, 70, 80, 90, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
  2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020
]
```

/api/v1/season/current

Return a list of all anime of the current year season.

Example output (truncated):

```json
[
  {
    "anime_id": 41380,
    "title": "100-man no Inochi no Ue ni Ore wa Tatteiru | I'm Standing on a Million Lives",
    "cover": "https://cdn.myanimelist.net/images/anime/1825/108800.jpg",
    "year": "2020",
    "season": "Fall 2020",
    "themes": ["41380-00", "41380-01", "41380-02"],
    "__type__": "Anime"
  }
]
```

/api/v1/season/:year

Return a list of all anime of the year divided by seasons.

Example output (truncated):

/api/v1/season/2019

```json
{
  "year": 2019,
  "seasons": [
    {
      "season": "Winter",
      "anime": [
        {
          "mal_id": 37956,
          "title": ["3D Kanojo: Real Girl 2nd Season"],
          "cover": "https://cdn.myanimelist.net/images/anime/1941/97219.jpg",
          "year": 2019,
          "season": "Winter 2019",
          "themes": [
            {
              "title": "Futari nara",
              "theme_id": "37956-00",
              "type": "OP",
              "artist": "BiSH",
              "mirrors": [
                {
                  "quality": "",
                  "mirror": "https://animethemes.moe/video/3DKanojoS2-OP1.webm",
                  "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/37956-00/0/audio"
                },
                {
                  "quality": "NC, BD, 1080",
                  "mirror": "https://animethemes.moe/video/3DKanojoS2-OP1-NCBD1080.webm",
                  "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/37956-00/1/audio"
                }
              ],
              "notes": "",
              "episodes": "",
              "category": ""
            }
          ]
        }
      ]
    },
    {
      "season": "Spring",
      "anime": [
        {
          "mal_id": 38735,
          "title": ["7 Seeds", "7SEEDS"],
          "cover": "https://cdn.myanimelist.net/images/anime/1305/96703.jpg",
          "year": 2019,
          "season": "Spring 2019",
          "themes": [
            {
              "title": "Ark",
              "theme_id": "38735-00",
              "type": "OP",
              "artist": null,
              "mirrors": [
                {
                  "quality": "",
                  "mirror": "https://animethemes.moe/video/7Seeds-OP1.webm",
                  "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/38735-00/0/audio"
                }
              ],
              "notes": "",
              "episodes": "",
              "category": ""
            }
          ]
        }
      ]
    },
    {
      "season": "Summer",
      "anime": [
        {
          "mal_id": 38753,
          "title": [
            "Araburu Kisetsu no Otome-domo yo.",
            "O Maidens in Your Savage Season"
          ],
          "cover": "https://cdn.myanimelist.net/images/anime/1256/101166.jpg",
          "year": 2019,
          "season": "Summer 2019",
          "themes": [
            {
              "title": "Otome-domo yo",
              "theme_id": "38753-00",
              "type": "OP V1",
              "artist": "CHiCO",
              "mirrors": [
                {
                  "quality": "",
                  "mirror": "https://animethemes.moe/video/Araoto-OP1.webm",
                  "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/38753-00/0/audio"
                }
              ],
              "notes": "",
              "episodes": "1-4",
              "category": ""
            }
          ]
        }
      ]
    },
    {
      "season": "Fall",
      "anime": [
        {
          "mal_id": 38670,
          "title": ["Actors: Songs Connection"],
          "cover": "https://cdn.myanimelist.net/images/anime/1383/103339.jpg",
          "year": 2019,
          "season": "Fall 2019",
          "themes": [
            {
              "title": "Titania",
              "theme_id": "38670-00",
              "type": "OP",
              "artist": null,
              "mirrors": [
                {
                  "quality": "",
                  "mirror": "https://animethemes.moe/video/Actors-OP1.webm",
                  "audio": "http://animethemes-api.herokuapp.com/api/v1/theme/38670-00/0/audio"
                }
              ],
              "notes": "",
              "episodes": "",
              "category": ""
            }
          ]
        }
      ]
    }
  ]
}
```

### Get MyAnimeList or AniList anime list

#### MyAnimeList

/api/v1/mal/:user

/api/v1/mal/:user/:list_filter

Returns a list of the anime in the requested list identified by 'user' (MyAnimeList username) that are available in the data base.

Available filters:

- All: 7
- Watching: 1
- Completed: 2
- On hold: 3
- Dropped: 4
- Planning: 6

#### AniList

/api/v1/anilist/:user

/api/v1/anilist/:user/:list_filter

Returns a list of the anime in the requested list identified by 'user' (AniList username) that are available in the data base.

Available filters:

- 'CURRENT'
- 'PLANNING'
- 'COMPLETED'
- 'DROPPED'
- 'PAUSED'
- 'REPEATING'
