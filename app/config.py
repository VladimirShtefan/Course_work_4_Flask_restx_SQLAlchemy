from app.constants import DATA_BASE_PATH


class Config(object):
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATA_BASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {
        'ensure_ascii': False,
    }
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False
    DEBUG = False
    TESTING = False
    ERROR_INCLUDE_MESSAGE = False


class DevConfig(Config):
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = 1
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    ENV = 'production'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True
    # SQLALCHEMY_ECHO = True
