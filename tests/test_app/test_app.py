from flask import g

from app.fixtures.data import DATA


def test_app(client, database):
    with client.get('/'):
        assert getattr(g, 'session') == database.session


def test_data_fixture():
    assert isinstance(DATA, dict)
