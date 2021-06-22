import os


class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    JSON_SORT_KEYS = False


class Production(Config):
    DEBUG = False
    JSON_SORT_KEYS = False


config = {
    'development': DevelopmentConfig,
    'production': Production,
}
