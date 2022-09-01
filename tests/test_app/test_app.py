from flask import g

from app.fixtures.data import DATA


def test_app(client, database):
    with client.get('/'):
        assert getattr(g, 'session') == database.session


# def test_app_exception(client):
#     with patch('app.app.db') as mock:
#         mock.session.side_effect = DBAPIError
#         with pytest.raises(DBAPIError):
#             client.get('/')

def test_data_fixture():
    assert isinstance(DATA, dict)
