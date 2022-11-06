import os

from dotenv import load_dotenv

from app.constants import DATA_BASE_PATH

load_dotenv()


class Config(object):
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{DATA_BASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {
        'ensure_ascii': False,
    }
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False
    DEBUG = False
    TESTING = False
    ERROR_INCLUDE_MESSAGE = False
    ITEMS_PER_PAGE = 12
    CORS_HEADERS = 'Content-Type'
    ORIGINS = ['http://localhost:80',
               'http://vshtefan.ga:80',
               'http://localhost:5000']


class DevConfig(Config):
    ENV = 'development'
    TEMPLATES_AUTO_RELOAD = 1
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', 5432),
        db_name=os.getenv('POSTGRES_DB')
    )


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    ORIGINS = '*'
