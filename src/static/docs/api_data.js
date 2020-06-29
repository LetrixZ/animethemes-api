define({ "api": [
  {
    "type": "get",
    "url": "/current",
    "title": "Request list of anime and themes of the current season",
    "name": "current_season",
    "group": "Anime",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n     ...\n     {\n       \"malId\":40060,\n       \"title\":[\n          \"BNA\",\n          \"Brand New Animal\"\n       ],\n       \"cover\":\"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n       \"season\":\"Spring 2020\",\n       \"year\":2020,\n       \"themes\":[\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V1\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\"\n                }\n             ],\n             \"episodes\":\"1-5\",\n             \"notes\":\"\"\n          },\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V2\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\"\n                }\n             ],\n             \"episodes\":\"6-11\",\n             \"notes\":\"\"\n          },\n          ...\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Anime"
  },
  {
    "type": "get",
    "url": "/anime/:mal_id",
    "title": "Request anime and themes with MyAnimeList's anime id",
    "name": "get_anime",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "mal_id",
            "description": "<p>MyAnimeList's anime id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n   \"malId\":13601,\n   \"title\":[\n      \"Psycho Pass\",\n      \"Psychopath\"\n   ],\n   \"cover\":\"https://cdn.myanimelist.net/images/anime/5/43399.jpg\",\n   \"season\":\"Fall 2012\",\n   \"year\":2012,\n   \"themes\":[\n      {\n         \"title\":\"abnormalize\",\n         \"type\":\"OP1\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-OP1.webm\"\n            }\n         ],\n         \"episodes\":\"1-11\",\n         \"notes\":\"\"\n      },\n      {\n         \"title\":\"Out of Control\",\n         \"type\":\"OP2 V1\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-OP2v2.webm\"\n            }\n         ],\n         \"episodes\":\"12\",\n         \"notes\":\"\"\n      },\n      {\n         \"title\":\"Out of Control\",\n         \"type\":\"OP2 V2\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-OP2.webm\"\n            }\n         ],\n         \"episodes\":\"13-22\",\n         \"notes\":\"\"\n      },\n      {\n         \"title\":\"Namae no nai Kaibutsu\",\n         \"type\":\"ED1 V1\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-ED1.webm\"\n            }\n         ],\n         \"episodes\":\"1-3, 5, 7-8, 10-11\",\n         \"notes\":\"\"\n      },\n      {\n         \"title\":\"Namae no nai Kaibutsu\",\n         \"type\":\"ED1 V2\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-ED1v2.webm\"\n            }\n         ],\n         \"episodes\":\"4, 6, 9\",\n         \"notes\":\"\"\n      },\n      {\n         \"title\":\"All Alone With You\",\n         \"type\":\"ED2 V1\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-ED2.webm\"\n            }\n         ],\n         \"episodes\":\"12-21\",\n         \"notes\":\"\"\n      },\n      {\n         \"title\":\"All Alone With You\",\n         \"type\":\"ED2 V2\",\n         \"mirror\":[\n            {\n               \"quality\":\"NC, BD, 1080, Over\",\n               \"mirrorUrl\":\"https://animethemes.moe/video/PsychoPass-ED2v2.webm\"\n            }\n         ],\n         \"episodes\":\"22\",\n         \"notes\":\"Spoiler\"\n      }\n   ]\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Anime"
  },
  {
    "type": "get",
    "url": "/year/:year",
    "title": "Request list of anime and themes of the year",
    "name": "get_year",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n     ...\n     {\n       \"malId\":40060,\n       \"title\":[\n          \"BNA\",\n          \"Brand New Animal\"\n       ],\n       \"cover\":\"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n       \"season\":\"Spring 2020\",\n       \"year\":2020,\n       \"themes\":[\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V1\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\"\n                }\n             ],\n             \"episodes\":\"1-5\",\n             \"notes\":\"\"\n          },\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V2\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\"\n                }\n             ],\n             \"episodes\":\"6-11\",\n             \"notes\":\"\"\n          },\n          ...\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Anime"
  },
  {
    "type": "get",
    "url": "/search/:search_term",
    "title": "Perform a search on the DB to check for results based on search term",
    "name": "search_anime",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "search_term",
            "description": "<p>Search term</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n     ...\n     {\n       \"malId\":40060,\n       \"title\":[\n          \"BNA\",\n          \"Brand New Animal\"\n       ],\n       \"cover\":\"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n       \"season\":\"Spring 2020\",\n       \"year\":2020,\n       \"themes\":[\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V1\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\"\n                }\n             ],\n             \"episodes\":\"1-5\",\n             \"notes\":\"\"\n          },\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V2\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\"\n                }\n             ],\n             \"episodes\":\"6-11\",\n             \"notes\":\"\"\n          },\n          ...\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Anime"
  },
  {
    "type": "get",
    "url": "/season/:year/:season",
    "title": "Request list of anime and themes based on year and season",
    "name": "season",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n     ...\n     {\n       \"malId\":40060,\n       \"title\":[\n          \"BNA\",\n          \"Brand New Animal\"\n       ],\n       \"cover\":\"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n       \"season\":\"Spring 2020\",\n       \"year\":2020,\n       \"themes\":[\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V1\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\"\n                }\n             ],\n             \"episodes\":\"1-5\",\n             \"notes\":\"\"\n          },\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V2\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\"\n                }\n             ],\n             \"episodes\":\"6-11\",\n             \"notes\":\"\"\n          },\n          ...\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Anime"
  },
  {
    "type": "get",
    "url": "/seasons/:year/",
    "title": "Request list of seasons based on year",
    "name": "year_seasons",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "year",
            "description": "<p>Year</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "seasons",
            "description": "<p>Seasons of the year</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.season",
            "description": "<p>Season of the year</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "seasons.animes",
            "description": "<p>List of animes of the season</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "seasons.animes.malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "seasons.animes.title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "seasons.animes.year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "seasons.animes.themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "seasons.animes.themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n   \"year\":\"2000\",\n   \"seasons\":[\n      {\n         \"season\":\"Fall\",\n         \"animes\":[\n            {\n               \"malId\":1281,\n               \"title\":[\n                  \"Gakkou no Kaidan\",\n                  \"Ghost Stories\"\n               ],\n               \"cover\":\"https://cdn.myanimelist.net/images/anime/9/18360.jpg\",\n               \"season\":\"Fall 2000\",\n               \"year\":2000,\n               \"themes\":[\n                  {\n                     \"title\":\"Grow Up\",\n                     \"type\":\"OP\",\n                     \"mirror\":[\n                        {\n                           \"quality\":\"NC, DVD, 480\",\n                           \"mirrorUrl\":\"https://animethemes.moe/video/GakkouNoKaidan-OP1.webm\"\n                        }\n                     ],\n                     \"episodes\":\"\",\n                     \"notes\":\"\"\n                  },\n                  {\n                     \"title\":\"sexy sexy\",\n                     \"type\":\"ED\",\n                     \"mirror\":[\n                        {\n                           \"quality\":\"NC, DVD, 480\",\n                           \"mirrorUrl\":\"https://animethemes.moe/video/GakkouNoKaidan-ED1.webm\"\n                        }\n                     ],\n                     \"episodes\":\"\",\n                     \"notes\":\"\"\n                  }\n               ]\n            },\n            ...\n         ]\n      },\n      ...\n  ]\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Anime"
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-api\\src\\doc\\main.js",
    "groupTitle": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-api\\src\\doc\\main.js",
    "name": ""
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./static/docs/main.js",
    "group": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-api\\src\\static\\docs\\main.js",
    "groupTitle": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-api\\src\\static\\docs\\main.js",
    "name": ""
  },
  {
    "type": "get",
    "url": "/years",
    "title": "Request list of years available on the DB",
    "name": "get_seasons",
    "group": "Data",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "years",
            "description": "<p>List years and seasons</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "years.year",
            "description": "<p>Year</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "year.seasons",
            "description": "<p>Seasons of the year</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n    {\n       \"year\":2020,\n       \"seasons\":[\n          \"Spring\",\n          \"Winter\"\n       ]\n    },\n    {\n       \"year\":2019,\n       \"seasons\":[\n          \"Fall\",\n          \"Summer\",\n          \"Spring\",\n          \"Winter\"\n       ]\n    },\n    {\n       \"year\":2018,\n       \"seasons\":[\n          \"Spring\",\n          \"Fall\",\n          \"Summer\",\n          \"Winter\"\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Data"
  },
  {
    "type": "get",
    "url": "/years",
    "title": "Request list of years available on the DB",
    "name": "get_years",
    "group": "Data",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "years",
            "description": "<p>List years</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,90,80,70,60]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "Data"
  },
  {
    "type": "get",
    "url": "/anilist/:anilist_user",
    "title": "Request AniList's user list",
    "name": "get_anilist",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "mal_user",
            "description": "<p>AniList's username</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n     ...\n     {\n       \"malId\":40060,\n       \"title\":[\n          \"BNA\",\n          \"Brand New Animal\"\n       ],\n       \"cover\":\"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n       \"season\":\"Spring 2020\",\n       \"year\":2020,\n       \"themes\":[\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V1\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\"\n                }\n             ],\n             \"episodes\":\"1-5\",\n             \"notes\":\"\"\n          },\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V2\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\"\n                }\n             ],\n             \"episodes\":\"6-11\",\n             \"notes\":\"\"\n          },\n          ...\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "User"
  },
  {
    "type": "get",
    "url": "/user/:mal_user",
    "title": "Request MyAnimeList's user list",
    "name": "get_mal_list",
    "group": "User",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "mal_user",
            "description": "<p>MyAnimeList's username</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "malId",
            "description": "<p>MyAnimeList's id for the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "title",
            "description": "<p>Title and synonims of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "cover",
            "description": "<p>URL of the anime cover</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "season",
            "description": "<p>Season of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "year",
            "description": "<p>Year of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes",
            "description": "<p>List of themes</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.title",
            "description": "<p>Title of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.type",
            "description": "<p>Type of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.mirror",
            "description": "<p>List of mirrors for the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.quality",
            "description": "<p>Quality of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.mirror.mirrorUrl",
            "description": "<p>URL of the mirror</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.episodes",
            "description": "<p>Episodes of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.notes",
            "description": "<p>Notes of the theme</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": " [\n     ...\n     {\n       \"malId\":40060,\n       \"title\":[\n          \"BNA\",\n          \"Brand New Animal\"\n       ],\n       \"cover\":\"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n       \"season\":\"Spring 2020\",\n       \"year\":2020,\n       \"themes\":[\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V1\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\"\n                }\n             ],\n             \"episodes\":\"1-5\",\n             \"notes\":\"\"\n          },\n          {\n             \"title\":\"Ready to\",\n             \"type\":\"OP V2\",\n             \"mirror\":[\n                {\n                   \"quality\":\"default\",\n                   \"mirrorUrl\":\"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\"\n                }\n             ],\n             \"episodes\":\"6-11\",\n             \"notes\":\"\"\n          },\n          ...\n       ]\n    },\n    ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "User"
  }
] });
