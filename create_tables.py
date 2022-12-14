from app.app import create_app, get_config
from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.dao.model.user import Users
from app.dao.model.user_movie import UserMovie
from app.setup_db import db


def _create_tables():
    db.create_all()
    print('База создана')


if __name__ == '__main__':
    config = get_config()
    app = create_app(config)
    with app.app_context():
        _create_tables()
