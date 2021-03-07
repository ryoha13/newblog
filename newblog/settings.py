import os


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Operations:
    CONFIRM = 'confirm account'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

    BLOG_PER_PAGE = 5

    ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)


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
