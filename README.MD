# AnimeThemes API

AnimeThemes API is an unofficial API that gathers data from the subrredit r/AnimeThemes. 

## Deployment

Deployed on Heroku

[https://animethemes-api.herokuapp.com/api/v1](https://animethemes-api.herokuapp.com/api/v1)

## Usage

#### GET /anime/[id]
[id] = MyAnimeList's anime ID (Example: [40060](https://myanimelist.net/anime/40060))

##### Response
```json5
// ID = 40060
{
  "malId": 40060,
  "title": [
    "BNA",
    "Brand New Animal"
  ],
  "cover": "https://cdn.myanimelist.net/images/anime/1139/106986.jpg",
  "season": "Spring 2020",
  "year": 2020,
  "themes": [
    {
      "title": "Ready to",
      "type": "OP V1",
      "mal_id": 40060,
      "theme_id": "40060-0",
      "notes": "",
      "views": 0,
      "mirrors": [
        {
          "quality": "default",
          "mirrorUrl": "https://animethemes.moe/video/BrandNewAnimal-OP1.webm",
          "appUrl": "40060/0/0"
        }
      ]
    },
    //...
  ]
}
```

### GET /s/[name]
[name] = Anime's name (Example: Darling)

##### Response
````json5
// Name = Darling
[
  {
    "malId": 35849,
    "title": [
      "Darling in the FranXX"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/1614/90408.jpg",
    "season": "Winter 2018",
    "year": 2018,
    "themes": [
      {
        "title": "KISS OF DEATH (Produced by HYDE)",
        "type": "OP1 V1",
        "mal_id": 35849,
        "theme_id": "35849-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/DarlingInTheFranXX-OP1.webm",
            "appUrl": "35849/0/0"
          },
          {
            "quality": "NC, BD, 1080",
            "mirrorUrl": "https://animethemes.moe/video/DarlingInTheFranXX-OP1-NCBD1080.webm",
            "appUrl": "35849/0/1"
          }
        ]
      },
      //...
    ]
  }
]
````

### GET /s/theme/[name]
[name] = Theme's name (Example: Styx Helix)

#### Response
```json5
// Name = Styx Helix
[
  {
    "malId": 31240,
    "title": [
      "Re:Zero kara Hajimeru Isekai Seikatsu",
      "Re:ZERO -Starting Life in Another World-",
      "Re: Life in a different world from zero",
      "ReZero"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/11/79410.jpg",
    "season": "Spring 2016",
    "year": 2016,
    "themes": [
      {
        "title": "STYX HELIX",
        "type": "ED1 V1",
        "mal_id": 31240,
        "theme_id": "31240-2",
        "notes": "Spoiler",
        "views": 0,
        "mirrors": [
          {
            "quality": "BD, 1080, Over",
            "mirrorUrl": "https://animethemes.moe/video/ReZero-ED1v2.webm",
            "appUrl": "31240/2/0"
          }
        ]
      }
    ]
  },
  // ...
]
```

### GET /anime/[id]/[theme]/[quality]
[id] = MyAnimeList's anime ID (Example: [35062](https://myanimelist.net/anime/35062))

[theme] = Theme's index (Example: 0)

[quality] = Mirror's index (Example: 2)

#### Response
```text
// ID = 35062
// Theme = 0
// Quality = 2
Redirect to https://animethemes.moe/video/MahoutsukaiNoYome-OP1-NCBD1080.webm 
```

### GET /anime/[id]/[theme]/[quality]/audio
[id] = MyAnimeList's anime ID (Example: [35062](https://myanimelist.net/anime/35062))

[theme] = Theme's index (Example: 0)

[quality] = Mirror's index (Example: 2)

#### Response
```text
// ID = 35062
// Theme = 0
// Quality = 2
Redirect url to download MP3 version of the theme.
```

### GET /year/[year]
[year] = Year to get list of animes (Example: 2020)

#### Response
````json5
// Year = 2020
[
  {
    "malId": 38843,
    "title": [
      "Shironeko Project: Zero Chronicle",
      "Shironeko Project ZERO Chronicle"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/1494/105719.jpg",
    "season": "Spring 2020",
    "year": 2020,
    "themes": [
      {
        "title": "Tenbin -Libra-",
        "type": "OP",
        "mal_id": 38843,
        "theme_id": "38843-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/ShironekoProject-OP1.webm",
            "appUrl": "38843/0/0"
          }
        ]
      },
      {
        "title": "through the dark",
        "type": "ED1",
        "mal_id": 38843,
        "theme_id": "38843-1",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/ShironekoProject-ED1.webm",
            "appUrl": "38843/1/0"
          }
        ]
      },
      {
        "title": "Yasashiki Yami no Uta",
        "type": "ED2",
        "mal_id": 38843,
        "theme_id": "38843-2",
        "notes": "Spoiler",
        "views": 0,
        "mirrors": [
          {
            "quality": "Trans",
            "mirrorUrl": "https://animethemes.moe/video/ShironekoProject-ED2.webm",
            "appUrl": "38843/2/0"
          }
        ]
      }
    ]
  },
  //...
]
````

### GET /seasons/
Returns a list of seasons in the database

#### Response
```json5
[
  {
    "year": 2020,
    "seasons": [
      "Spring",
      "Winter",
      "Summer"
    ]
  },
  {
    "year": 2019,
    "seasons": [
      "Spring",
      "Fall",
      "Summer",
      "Winter"
    ]
  },
  //...
]
```


### GET /seasons/[year]
[year] = Year to get a list of animes divided by seasons (Example: 2020)

#### Response
```json5
// Year = 2020
{
  "year": "2020",
  "seasons": [
    {
      "season": "Spring",
      "animes": [
        {
          "malId": 40532,
          "title": [
            "Appare-Ranman!"
          ],
          "cover": "https://cdn.myanimelist.net/images/anime/1710/106614.jpg",
          "season": "Spring 2020",
          "year": 2020,
          "themes": [
            {
              "title": "I got it!",
              "type": "OP",
              "mal_id": 40532,
              "theme_id": "40532-0",
              "notes": "",
              "views": 0,
              "mirrors": [
                {
                  "quality": "default",
                  "mirrorUrl": "https://animethemes.moe/video/AppareRanman-OP1.webm",
                  "appUrl": "40532/0/0"
                }
              ]
            },
            {
              "title": "I'm Nobody",
              "type": "ED",
              "mal_id": 40532,
              "theme_id": "40532-1",
              "notes": "",
              "views": 0,
              "mirrors": [
                {
                  "quality": "default",
                  "mirrorUrl": "https://animethemes.moe/video/AppareRanman-ED1.webm",
                  "appUrl": "40532/1/0"
                }
              ]
            }
          ]
        },
        //...
      ]
    },
    {
      "season": "Summer",
      "animes": [
        {
          "malId": 40056,
          "title": [
            "Deca-Dence"
          ],
          "cover": "https://cdn.myanimelist.net/images/anime/1627/107552.jpg",
          "season": "Summer 2020",
          "year": 2020,
          "themes": [
            {
              "title": "Theater of Life",
              "type": "OP",
              "mal_id": 40056,
              "theme_id": "40056-0",
              "notes": "",
              "views": 0,
              "mirrors": [
                {
                  "quality": "default",
                  "mirrorUrl": "https://animethemes.moe/video/DecaDence-OP1.webm",
                  "appUrl": "40056/0/0"
                }
              ]
            },
            //...
          ]
        },
        //...
      ]
    }
  ]
}
```

### GET /seasons/[year]/[season]
[year] = Year to get animes divided by seasons (Example: 2019)

[season] = Season of the year (Example: Summer)

#### Response
````json5
// Year = 2020
// Season = Summer
[
  {
    "malId": 38753,
    "title": [
      "Araburu Kisetsu no Otome-domo yo.",
      "O Maidens in Your Savage Season"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/1256/101166.jpg",
    "season": "Summer 2019",
    "year": 2019,
    "themes": [
      {
        "title": "Otome-domo yo",
        "type": "OP V1",
        "mal_id": 38753,
        "theme_id": "38753-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/Araoto-OP1.webm",
            "appUrl": "38753/0/0"
          },
          {
            "quality": "Lyrics",
            "mirrorUrl": "https://animethemes.moe/video/Araoto-OP1-Lyrics.webm",
            "appUrl": "38753/0/1"
          }
        ]
      },
      //...
    ]
  },
  //... 
]
````


### GET /mal/[username]
[username] = MyAnimeList's username (Example: Letrix)

#### Response
````json5
// Username = Letrix
[
  {
    "malId": 40148,
    "title": [
      "22/7",
      "Nanabun no Nijyuuni"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/1810/104530.jpg",
    "season": "Winter 2020",
    "year": 2020,
    "themes": [
      {
        "title": "Muzui",
        "type": "OP",
        "mal_id": 40148,
        "theme_id": "40148-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/NanabunNoNijyuuni-OP1.webm",
            "appUrl": "40148/0/0"
          }
        ]
      },
      //...
    ]
  },
  //...
]
````


### GET /anilist/[username]
[username] = AnimeList's username (Example: Letrix)

#### Response
````json5
// Username = Letrix
[
  {
    "malId": 40148,
    "title": [
      "22/7",
      "Nanabun no Nijyuuni"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/1810/104530.jpg",
    "season": "Winter 2020",
    "year": 2020,
    "themes": [
      {
        "title": "Muzui",
        "type": "OP",
        "mal_id": 40148,
        "theme_id": "40148-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/NanabunNoNijyuuni-OP1.webm",
            "appUrl": "40148/0/0"
          }
        ]
      },
      //...
    ]
  },
  //...
]
````


### GET /current/
Returns a list of animes of the current season (Summer 2020 [2020/08/05])

#### Response
````json5
[
  {
    "malId": 40839,
    "title": [
      "Kanojo, Okarishimasu",
      "Rent-a-Girlfriend",
      "Kanokari"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/1485/107693.jpg",
    "season": "Summer 2020",
    "year": 2020,
    "themes": [
      {
        "title": "Centimeter",
        "type": "OP",
        "mal_id": 40839,
        "theme_id": "40839-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/Kanokari-OP1.webm",
            "appUrl": "40839/0/0"
          }
        ]
      },
      {
        "title": "Kokuhaku Bungee Jump",
        "type": "ED V1",
        "mal_id": 40839,
        "theme_id": "40839-1",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/Kanokari-ED1.webm",
            "appUrl": "40839/1/0"
          }
        ]
      },
      {
        "title": "Kokuhaku Bungee Jump",
        "type": "ED V2",
        "mal_id": 40839,
        "theme_id": "40839-2",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "default",
            "mirrorUrl": "https://animethemes.moe/video/Kanokari-ED1v2.webm",
            "appUrl": "40839/2/0"
          }
        ]
      }
    ]
  },
  //...
]
````

### GET /latest/themes/
Returns a list of the latest added animes to the database

#### Response
````json5
[
  {
    "malId": 35062,
    "title": [
      "Mahoutsukai no Yome",
      "The Ancient Magus' Bride",
      "The Magician's Bride"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/3/88476.jpg",
    "season": "Fall 2017",
    "year": 2017,
    "themes": [
      {
        "title": "The Legend of 'The Ancient Magus Bride'",
        "type": "ED3",
        "mal_id": 35062,
        "theme_id": "35062-5",
        "notes": "Spoiler",
        "views": 0,
        "mirrors": [
          {
            "quality": "Trans, Subbed",
            "mirrorUrl": "https://animethemes.moe/video/MahoutsukaiNoYome-ED3.webm",
            "appUrl": "35062/5/0"
          }
        ]
      }
    ]
  },
  //..
]
````


### GET /latest/animes/
Returns a list of the animes added animes to the database

#### Response
````json5
[
  {
    "malId": 763,
    "title": [
      "Zoids",
      "Zoids Classic",
      "Zoids: Chaotic Century",
      "Zoids: Guardian Forces"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/2/15412.jpg",
    "season": "All",
    "year": 90,
    "themes": [
      {
        "title": "Wild Flowers",
        "type": "OP V1",
        "mal_id": 763,
        "theme_id": "763-0",
        "notes": "",
        "views": 0,
        "mirrors": [
          {
            "quality": "NC, BD, 974",
            "mirrorUrl": "https://animethemes.moe/video/Zoids-OP1.webm",
            "appUrl": "763/0/0"
          }
        ]
      },
      //...
    ]
  },
  //...
]
````

### GET /top/
Returns a list of the top 15 most watched themes

#### Response
````json5
[
  {
    "malId": 6547,
    "title": [
      "Angel Beats!"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/10/22061.jpg",
    "season": "Spring 2010",
    "year": 2010,
    "themes": [
      {
        "title": "My Soul, Your Beats!",
        "type": "OP2",
        "mal_id": 6547,
        "theme_id": "6547-1",
        "notes": "",
        "views": 4,
        "mirrors": [
          {
            "quality": "BD, 1080",
            "mirrorUrl": "https://animethemes.moe/video/AngelBeats-OP2.webm",
            "appUrl": "6547/1/0"
          }
        ]
      }
    ]
  },
  {
    "malId": 6547,
    "title": [
      "Angel Beats!"
    ],
    "cover": "https://cdn.myanimelist.net/images/anime/10/22061.jpg",
    "season": "Spring 2010",
    "year": 2010,
    "themes": [
      {
        "title": "My Soul, Your Beats!",
        "type": "OP1",
        "mal_id": 6547,
        "theme_id": "6547-0",
        "notes": "",
        "views": 3,
        "mirrors": [
          {
            "quality": "NC, BD, 1080",
            "mirrorUrl": "https://animethemes.moe/video/AngelBeats-OP1.webm",
            "appUrl": "6547/0/0"
          }
        ]
      }
    ]
  },
  //...
]
````

