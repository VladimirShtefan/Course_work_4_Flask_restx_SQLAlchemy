import os

from app.app import create_app
from app.config import Config, DevConfig, ProdConfig
from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.dao.model.user import User
from app.dao.model.user_movie import UserMovie
from app.setup_db import db


match os.environ.get('FLASK_ENV'):
    case 'development':
        app = create_app(DevConfig)
    case 'production':
        app = create_app(ProdConfig)
    case _:
        raise RuntimeError('Need to set environment variable FLASK_ENV')


def _create_tables():
    db.create_all()
    print('База создана')


if __name__ == '__main__':
    app = create_app(Config)
    with app.app_context():
        _create_tables()
