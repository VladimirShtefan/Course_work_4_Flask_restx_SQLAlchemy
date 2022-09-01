import pytest

from sqlalchemy.ext.declarative import declarative_base

from app.app import create_app
from app.config import TestConfig
from app.setup_db import db


@pytest.fixture
def app():
    _app = create_app(TestConfig)
    with _app.app_context():
        db.init_app(_app)
        yield _app


@pytest.fixture
def database(app):
    db.drop_all()
    db.create_all()
    db.session.commit()
    return db


@pytest.fixture
def client(database, app):
    with app.test_client() as client:
        yield client


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
                    field = value+i
                model[key] = field
            model_list.append(name_model(**model))
        database.session.add_all(model_list)
        database.session.commit()
        return model_list
    return wrapper
