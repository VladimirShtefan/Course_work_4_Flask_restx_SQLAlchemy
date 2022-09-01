from sqlalchemy.exc import IntegrityError

from app.app import create_app
from app.config import Config
from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.fixtures.data import DATA
from app.setup_db import db
from logger import create_logger

logger = create_logger('create_models')


def _load_fixtures(database=db):
    for movie in DATA["movies"]:
        m = Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"],
        )
        database.session.add(m)

    for director in DATA["directors"]:
        d = Director(
            id=director["pk"],
            director_name=director["director_name"],
        )
        database.session.add(d)

    for genre in DATA["genres"]:
        d = Genre(
            id=genre["pk"],
            genre_name=genre["genre_name"],
        )
        database.session.add(d)
    try:
        database.session.commit()
        logger.info('База создана успешно')
        print('База заполнена')
        database.session.close()
    except IntegrityError:
        logger.info('База уже создана или переданы не верные данные, проверьте базу')
        database.session.rollback()
        database.session.close()


if __name__ == '__main__':
    app = create_app(Config)
    with app.app_context():
        _load_fixtures()
