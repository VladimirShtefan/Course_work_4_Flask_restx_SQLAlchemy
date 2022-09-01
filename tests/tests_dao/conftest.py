import pytest


from app.dao.director import DirectorDAO
from app.dao.genre import GenreDAO
from app.dao.movie import MovieDAO


@pytest.fixture()
def genre_dao(database):
    return GenreDAO(database.session)


@pytest.fixture()
def movie_dao(database):
    return MovieDAO(database.session)


@pytest.fixture()
def director_dao(database):
    return DirectorDAO(database.session)
