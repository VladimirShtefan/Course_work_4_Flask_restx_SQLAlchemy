from unittest.mock import patch
from werkzeug.exceptions import NotFound

import pytest

from app.dao.model.movie import Movie
from app.dao.movie import MovieDAO
from app.service.movie import MovieService


class TestMovieService:
    @pytest.fixture()
    @patch('app.dao.movie.MovieDAO')
    def movie_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one_by_id.return_value = Movie(id=1, title='test_movie')
        dao.get_all_movies.return_value = [
            Movie(id=1, title='test_movie_1'),
            Movie(id=2, title='test_movie_2'),
        ]
        dao.add_movie.return_value = [
            Movie(id=1, title='test_movie_1'),
            Movie(id=2, title='test_movie_2'),
        ]
        dao.delete_row.return_value = None
        dao.put_movie.return_value = None
        return dao

    @pytest.fixture()
    def movie_service(self, movie_dao_mock):
        with patch.object(MovieService, '__init__', lambda self: None):
            movie = MovieService()
            movie.dao = movie_dao_mock
            yield movie

    @pytest.fixture
    def movie(self, database):
        obj = Movie(title="test_movie_1")
        database.session.add(obj)
        database.session.commit()
        return obj

    def test_get_movie(self, movie_service, movie):
        assert movie_service.get_movie(movie.id)

    def test_movie_not_found(self, movie_dao_mock, movie_service):
        movie_dao_mock.get_one_by_id.side_effect = NotFound
        with pytest.raises(NotFound):
            movie_service.get_movie(10)

    def test_add_movie(self, movie_dao_mock, movie_service, movie):
        new_movie = movie_service.add_movie()
        assert new_movie[1].id == 2

    @pytest.mark.parametrize('page', [1, None])
    def test_get_movies(self, movie_dao_mock, movie_service, page):
        movies = movie_service.get_movies()
        assert len(movies) == 2
        assert movies == movie_dao_mock.get_all_movies.return_value

    def test_del_item(self, movie_dao_mock, movie_service):
        assert movie_service.delete_movie(id=1) is None

    def test_put_movie(self, movie_dao_mock, movie_service):
        assert movie_service.put_movie(id=1) is None

    def test_init(self, database):
        service = MovieService()
        assert type(service.dao) == MovieDAO
