from functools import wraps
from unittest.mock import patch

import pytest

from app.dao.model.genre import Genre


class TestGenresView:

    @staticmethod
    def mock_decorator(*roles):
        def mock_mock_decorator(f):
            @wraps(f)
            def decorator(*args, **kwargs):
                return f(*args, **kwargs, email='email')
            return decorator
        return mock_mock_decorator

    @pytest.fixture
    def genre(self, database):
        obj = Genre(name="test_genre_1")
        database.session.add(obj)
        database.session.commit()
        return obj

    def test_many(self, client, genre):
        with patch('app.helpers.decorators.user_required', self.mock_decorator):
            response = client.get("/genres/")
            assert response.status_code == 200
            assert response.json == [{"id": genre.id, "name": genre.name}]

    def test_genre_pages(self, client, genre):
        response = client.get("/genres/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/genres/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_genre(self, client, genre):
        response = client.get("/genres/1/")
        assert response.status_code == 200
        assert response.json == {"id": genre.id, "name": genre.name}

    def test_genre_not_found(self, client, genre):
        response = client.get("/genres/2/")
        assert response.status_code == 404