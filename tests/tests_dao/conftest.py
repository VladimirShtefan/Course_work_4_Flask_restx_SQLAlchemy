import pytest
from sqlalchemy.ext.declarative import declarative_base


from app.dao.director import DirectorDAO
from app.dao.genre import GenreDAO
from app.dao.movie import MovieDAO
from app.dao.user import UserDAO


@pytest.fixture()
def genre_dao(database):
    return GenreDAO(database.session)


@pytest.fixture()
def movie_dao(database):
    return MovieDAO(database.session)


@pytest.fixture()
def director_dao(database):
    return DirectorDAO(database.session)


@pytest.fixture()
def user_dao(database):
    return UserDAO(database.session)


@pytest.fixture
def create_models(database):
    def wrapper(name_model: declarative_base, number_of_models: int, **fields):
        model_list = []
        for i in range(1, number_of_models+1):
            model = {}
            for key, value in fields.items():
                if isinstance(value, str):
                    field = f'{value}_{i}'
                else:
                    field = value+i if type(value) != bytes else value
                model[key] = field
            model_list.append(name_model(**model))
        database.session.add_all(model_list)
        database.session.commit()
        return model_list
    return wrapper
