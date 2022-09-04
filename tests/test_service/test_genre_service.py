from unittest.mock import patch
from werkzeug.exceptions import NotFound

import pytest

from app.dao.model.genre import Genre
from app.service.genre import GenreService


class TestGenreService:
    @pytest.fixture()
    @patch('app.dao.genre.GenreDAO')
    def genres_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one_by_id.return_value = Genre(id=1, name='test_genre')
        dao.get_all_items.return_value = [
            Genre(id=1, name='test_genre_1'),
            Genre(id=2, name='test_genre_2'),
        ]
        dao.add_genre.return_value = [
            Genre(id=1, name='test_genre_1'),
            Genre(id=2, name='test_genre_2'),
        ]
        return dao

    @pytest.fixture()
    def genres_service(self, genres_dao_mock):
        with patch.object(GenreService, '__init__', lambda self: None):
            genre = GenreService()
            genre.dao = genres_dao_mock
            yield genre

    @pytest.fixture
    def genre(self, database):
        obj = Genre(name="test_genre_1")
        database.session.add(obj)
        database.session.commit()
        return obj

    def test_get_genre(self, genres_service, genre):
        assert genres_service.get_item_by_id(genre.id)

    def test_genre_not_found(self, genres_dao_mock, genres_service):
        genres_dao_mock.get_one_by_id.side_effect = NotFound
        with pytest.raises(NotFound):
            genres_service.get_item_by_id(10)

    def test_add_genre(self, genres_dao_mock, genres_service, genre):
        new_genre = genres_service.add_genre()
        assert new_genre[1].id == 2

    @pytest.mark.parametrize('page', [1, None])
    def test_get_genres(self, genres_dao_mock, genres_service, page):
        genres = genres_service.get_all_items(page=page)
        assert len(genres) == 2
        assert genres == genres_dao_mock.get_all_items.return_value
        genres_dao_mock.get_all_items.assert_called_with(page=page)
