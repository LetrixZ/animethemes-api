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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n  \"malId\": 40060,\n  \"title\": [\n    \"BNA\",\n    \"Brand New Animal\"\n  ],\n  \"cover\": \"https://cdn.myanimelist.net/images/anime/1139/106986.jpg\",\n  \"season\": \"Spring 2020\",\n  \"year\": 2020,\n  \"themes\": [\n    {\n      \"title\": \"Ready to\",\n      \"type\": \"OP V1\",\n      \"mirror\": [\n        {\n          \"quality\": \"default\",\n          \"mirrorUrl\": \"https://animethemes.moe/video/BrandNewAnimal-OP1.webm\",\n          \"appUrl\": \"40060/0/0\"\n        }\n      ],\n      \"episodes\": \"1-5\",\n      \"notes\": \"\",\n      \"extras\": {\n        \"views\": 0,\n        \"likes\": 0,\n        \"dislikes\": 0,\n        \"malId\": 40060\n      },\n      \"audio\": {\n        \"artist\": \"Sumire Morohoshi\",\n        \"title\": \"Ready to\",\n        \"mirror\": \"https://dl4.wapkizfile.info/ddl/0d58ba3e38aa5c118d16200ecaad6d5b/osanime+wapkiz+com/audio.mp3\"\n      }\n    },\n    {\n      \"title\": \"Ready to\",\n      \"type\": \"OP V2\",\n      \"mirror\": [\n        {\n          \"quality\": \"default\",\n          \"mirrorUrl\": \"https://animethemes.moe/video/BrandNewAnimal-OP1v2.webm\",\n          \"appUrl\": \"40060/1/0\"\n        }\n      ],\n      \"episodes\": \"6-11\",\n      \"notes\": \"\",\n      \"extras\": {\n        \"views\": 0,\n        \"likes\": 0,\n        \"dislikes\": 0,\n        \"malId\": 40060\n      },\n      \"audio\": {\n        \"artist\": \"Sumire Morohoshi\",\n        \"title\": \"Ready to\",\n        \"mirror\": \"https://dl4.wapkizfile.info/ddl/0d58ba3e38aa5c118d16200ecaad6d5b/osanime+wapkiz+com/audio.mp3\"\n      }\n    },\n    {\n      \"title\": \"NIGHT RUNNING\",\n      \"type\": \"ED V1\",\n      \"mirror\": [\n        {\n          \"quality\": \"default\",\n          \"mirrorUrl\": \"https://animethemes.moe/video/BrandNewAnimal-ED1.webm\",\n          \"appUrl\": \"40060/2/0\"\n        }\n      ],\n      \"episodes\": \"1-6\",\n      \"notes\": \"\",\n      \"extras\": {\n        \"views\": 0,\n        \"likes\": 0,\n        \"dislikes\": 0,\n        \"malId\": 40060\n      },\n      \"audio\": {\n        \"artist\": \"Shin Sakiura Feat\",\n        \"title\": \"NIGHT RUNNING\",\n        \"mirror\": \"https://dl4.wapkizfile.info/ddl/c776e0444ba03e337e7ebc077df10fdf/osanime+wapkiz+com/audio.mp3\"\n      }\n    },\n    {\n      \"title\": \"NIGHT RUNNING\",\n      \"type\": \"ED V2\",\n      \"mirror\": [\n        {\n          \"quality\": \"default\",\n          \"mirrorUrl\": \"https://animethemes.moe/video/BrandNewAnimal-ED1v2.webm\",\n          \"appUrl\": \"40060/3/0\"\n        }\n      ],\n      \"episodes\": \"7-10\",\n      \"notes\": \"\",\n      \"extras\": {\n        \"views\": 0,\n        \"likes\": 0,\n        \"dislikes\": 0,\n        \"malId\": 40060\n      },\n      \"audio\": {\n        \"artist\": \"Shin Sakiura Feat\",\n        \"title\": \"NIGHT RUNNING\",\n        \"mirror\": \"https://dl4.wapkizfile.info/ddl/c776e0444ba03e337e7ebc077df10fdf/osanime+wapkiz+com/audio.mp3\"\n      }\n    },\n    {\n      \"title\": \"NIGHT RUNNING\",\n      \"type\": \"ED V3\",\n      \"mirror\": [\n        {\n          \"quality\": \"default\",\n          \"mirrorUrl\": \"https://animethemes.moe/video/BrandNewAnimal-ED1v3.webm\",\n          \"appUrl\": \"40060/4/0\"\n        }\n      ],\n      \"episodes\": \"11\",\n      \"notes\": \"\",\n      \"extras\": {\n        \"views\": 0,\n        \"likes\": 0,\n        \"dislikes\": 0,\n        \"malId\": 40060\n      },\n      \"audio\": {\n        \"artist\": \"Shin Sakiura Feat\",\n        \"title\": \"NIGHT RUNNING\",\n        \"mirror\": \"https://dl4.wapkizfile.info/ddl/c776e0444ba03e337e7ebc077df10fdf/osanime+wapkiz+com/audio.mp3\"\n      }\n    }\n  ]\n}",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 38843,\n    \"title\": [\n      \"Shironeko Project: Zero Chronicle\",\n      \"Shironeko Project ZERO Chronicle\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/1494/105719.jpg\",\n    \"season\": \"Spring 2020\",\n    \"year\": 2020,\n    \"themes\": [\n      {\n        \"title\": \"Tenbin -Libra-\",\n        \"type\": \"OP\",\n        \"mirror\": [\n          {\n            \"quality\": \"default\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/ShironekoProject-OP1.webm\",\n            \"appUrl\": \"38843/0/0\"\n          }\n        ],\n        \"episodes\": \"1-11\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 38843\n        },\n        \"audio\": {\n          \"artist\": \"Takanori Nishikawa + ASCA\",\n          \"title\": \"Tenbin  -Libra-\",\n          \"mirror\": \"https://dl4.wapkizfile.info/ddl/55e0a08edbdd816fdc15f97064b19436/osanime+wapkiz+com/audio.mp3\"\n        }\n      },\n      {\n        \"title\": \"through the dark\",\n        \"type\": \"ED1\",\n        \"mirror\": [\n          {\n            \"quality\": \"default\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/ShironekoProject-ED1.webm\",\n            \"appUrl\": \"38843/1/0\"\n          }\n        ],\n        \"episodes\": \"1-11\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 38843\n        },\n        \"audio\": {\n          \"artist\": \"Rei Yasuda\",\n          \"title\": \"through the dark\",\n          \"mirror\": \"https://dl4.wapkizfile.info/ddl/e308ad436d196f903715f4085dcc931f/osanime+wapkiz+com/audio.mp3\"\n        }\n      },\n      {\n        \"title\": \"Yasashiki Yami no Uta\",\n        \"type\": \"ED2\",\n        \"mirror\": [\n          {\n            \"quality\": \"Trans\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/ShironekoProject-ED2.webm\",\n            \"appUrl\": \"38843/2/0\"\n          }\n        ],\n        \"episodes\": \"12\",\n        \"notes\": \"Spoiler\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 38843\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
    "url": "/latest",
    "title": "Request list of the most recent added themes",
    "name": "latest_themes",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
    "url": "/top/:size",
    "title": "Request list of the most watched themes",
    "name": "most_watched",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "int",
            "optional": false,
            "field": "size",
            "description": "<p>Size of the list</p>"
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
    "url": "/themes/:theme_name",
    "title": "Search for a theme by its name",
    "name": "search_theme",
    "group": "Anime",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "theme_search",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "seasons.animes.themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "seasons.animes.themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "seasons.animes.themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "seasons.animes.themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "seasons.animes.themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "seasons.animes.themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "seasons.animes.themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n  \"year\": \"2020\",\n  \"seasons\": [\n    {\n      \"season\": \"Spring\",\n      \"animes\": [\n        {\n          \"malId\": 40532,\n          \"title\": [\n            \"Appare-Ranman!\"\n          ],\n          \"cover\": \"https://cdn.myanimelist.net/images/anime/1710/106614.jpg\",\n          \"season\": \"Spring 2020\",\n          \"year\": 2020,\n          \"themes\": [\n            {\n              \"title\": \"I got it!\",\n              \"type\": \"OP\",\n              \"mirror\": [\n                {\n                  \"quality\": \"default\",\n                  \"mirrorUrl\": \"https://animethemes.moe/video/AppareRanman-OP1.webm\",\n                  \"appUrl\": \"40532/0/0\"\n                }\n              ],\n              \"episodes\": \"1-\",\n              \"notes\": \"\",\n              \"extras\": {\n                \"views\": 0,\n                \"likes\": 0,\n                \"dislikes\": 0,\n                \"malId\": 40532\n              },\n              \"audio\": {\n                \"artist\": \"Mia REGINA\",\n                \"title\": \"I got it!\",\n                \"mirror\": \"https://dl4.wapkizfile.info/ddl/7b87353304746846d873ba0934fc8859/osanime+wapkiz+com/audio.mp3\"\n              }\n            },\n            {\n              \"title\": \"I'm Nobody\",\n              \"type\": \"ED\",\n              \"mirror\": [\n                {\n                  \"quality\": \"default\",\n                  \"mirrorUrl\": \"https://animethemes.moe/video/AppareRanman-ED1.webm\",\n                  \"appUrl\": \"40532/1/0\"\n                }\n              ],\n              \"episodes\": \"1-\",\n              \"notes\": \"\",\n              \"extras\": {\n                \"views\": 0,\n                \"likes\": 0,\n                \"dislikes\": 0,\n                \"malId\": 40532\n              },\n              \"audio\": {\n                \"artist\": \"Showtaro Morikubo\",\n                \"title\": \"Im Nobody\",\n                \"mirror\": \"https://dl4.wapkizfile.info/ddl/8ecae8e5649dfdca6eaa9c5b47367436/osanime+wapkiz+com/audio.mp3\"\n              }\n            }\n          ]\n        }, ...\n    ],\n    ...\n}",
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
    "group": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-app\\src\\doc\\main.js",
    "groupTitle": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-app\\src\\doc\\main.js",
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
    "group": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-app\\src\\static\\docs\\main.js",
    "groupTitle": "C:\\Users\\Fermin\\PycharmProjects\\animethemes-app\\src\\static\\docs\\main.js",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
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
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.extras",
            "description": "<p>Extras of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.views",
            "description": "<p>Views of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.likes",
            "description": "<p>Like count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.dislikes",
            "description": "<p>Dislike count of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "int",
            "optional": false,
            "field": "themes.extras.malId",
            "description": "<p>MalID of the anime</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "themes.audio",
            "description": "<p>Audio data of the theme</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.artist",
            "description": "<p>Artist of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.title",
            "description": "<p>Title of the original song</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "themes.audio.mirror",
            "description": "<p>Mirror link of the original song</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"malId\": 851,\n    \"title\": [\n      \"Kyou kara Ore wa!!\"\n    ],\n    \"cover\": \"https://cdn.myanimelist.net/images/anime/2/43779.jpg\",\n    \"season\": \"All\",\n    \"year\": 90,\n    \"themes\": [\n      {\n        \"title\": \"Bokura Wa Family\",\n        \"type\": \"ED\",\n        \"mirror\": [\n          {\n            \"quality\": \"BD, 1080\",\n            \"mirrorUrl\": \"https://animethemes.moe/video/KyouKaraOreWa-ED1.webm\",\n            \"appUrl\": \"851/0/0\"\n          }\n        ],\n        \"episodes\": \"\",\n        \"notes\": \"\",\n        \"extras\": {\n          \"views\": 0,\n          \"likes\": 0,\n          \"dislikes\": 0,\n          \"malId\": 851\n        },\n        \"audio\": {\n          \"artist\": null,\n          \"title\": null,\n          \"mirror\": null\n        }\n      }\n    ]\n  },\n  ...\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.py",
    "groupTitle": "User"
  }
] });
