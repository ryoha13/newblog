import os


class Operations:
    pass


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_URI')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_URI')


class ProConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PRO_URI')


configs = {
    'dev': DevConfig,
    'test': TestConfig,
    'pro': ProConfig
}
