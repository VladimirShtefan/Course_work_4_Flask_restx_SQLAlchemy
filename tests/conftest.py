from functools import wraps
from unittest.mock import patch


def mock_decorator(*roles):
    def mock_mock_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            return f(*args, **kwargs, email='email')

        return decorator

    return mock_mock_decorator


patch('app.helpers.decorators.user_required', mock_decorator).start()


import pytest

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
