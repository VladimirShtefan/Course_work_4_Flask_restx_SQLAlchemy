from unittest.mock import patch
from werkzeug.exceptions import NotFound

import pytest

from app.dao.model.user import Users, Role
from app.dao.user import UserDAO
from app.exceptions import ValidationError, UserNotFound, InvalidPassword
from app.service.user import UserService


class TestUserService:
    @pytest.fixture()
    @patch('app.dao.user.UserDAO')
    def user_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.search_user.return_value = Users(id=1, email='email',
                                             password=b"\x1e\xbe'7C\x9b\x8fZ\xa7k^%\xff\x10\xb0G\xfa\xf5\x17\xbb\xa6l\xe7\xe3y\xc8\x9a<\x94\x98{y\x9d\xc1\x83\x17\x1e\xd5%\xf0Z\xc2\x13\x8em>\xd54\xc5\xf6\r\xff,y\xba\xce\x9e\x99\x9a;\x18\t\xd6\x1c",
                                             role=Role.user)
        dao.create_user.return_value = None
        # dao.add_movie.return_value = [
        #     Movie(id=1, title='test_movie_1'),
        #     Movie(id=2, title='test_movie_2'),
        # ]
        # dao.delete_row.return_value = None
        # dao.put_movie.return_value = None
        return dao

    @pytest.fixture()
    @patch('app.dao.user.UserDAO')
    def user_none_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.search_user.return_value = None
        return dao

    @pytest.fixture()
    def user_service(self, user_dao_mock):
        with patch.object(UserService, '__init__', lambda self: None):
            user = UserService()
            user.dao = user_dao_mock
            yield user

    @pytest.fixture()
    def user_service_none(self, user_none_dao_mock):
        with patch.object(UserService, '__init__', lambda self: None):
            user = UserService()
            user.dao = user_none_dao_mock
            yield user

    # @pytest.fixture
    # def movie(self, database):
    #     obj = Movie(title="test_movie_1")
    #     database.session.add(obj)
    #     database.session.commit()
    #     return obj
    #
    def test_get_hash(self, user_service):
        password = user_service.get_hash('password')
        print(password)
        assert isinstance(password, bytes)

    def test_check_reliability(self, user_service):
        password = user_service.check_reliability('Intafy*D1411')
        assert password == 'Intafy*D1411'
        with pytest.raises(ValidationError):
            user_service.check_reliability('1411')

    def test_add_data_for_token(self, user_service):
        token = user_service.add_data_for_token({'minutes': 2}, {'user': 'user'})
        assert isinstance(token, str)

    def test_generate_tokens(self, user_service):
        tokens = user_service.generate_tokens({'user': 'user'})
        assert isinstance(tokens, dict)

    def test_search_user(self, user_service):
        tokens = user_service.search_user(email='email', password='password')
        assert isinstance(tokens, dict)
        with pytest.raises(InvalidPassword):
            user_service.search_user(email='email', password='password1')

    def test_search_user_exception(self, user_service_none):
        with pytest.raises(UserNotFound):
            user_service_none.search_user(email='email', password='password')

    def test_create_user(self, user_service):
        assert user_service.create_user(email='email', password='sfsdfsdfdsSADFASD65456@!#@!#', role='admin') is None
        assert user_service.create_user(email='email', password='sfsdfsdfdsSADFASD65456@!#@!#', role='') is None

    # def test_get_movie(self, movie_service, movie):
    #     assert movie_service.get_movie(movie.id)
    #
    # def test_movie_not_found(self, movie_dao_mock, movie_service):
    #     movie_dao_mock.get_one_by_id.side_effect = NotFound
    #     with pytest.raises(NotFound):
    #         movie_service.get_movie(10)
    #
    # def test_add_movie(self, movie_dao_mock, movie_service, movie):
    #     new_movie = movie_service.add_movie()
    #     assert new_movie[1].id == 2
    #
    # @pytest.mark.parametrize('page', [1, None])
    # def test_get_movies(self, movie_dao_mock, movie_service, page):
    #     movies = movie_service.get_movies()
    #     assert len(movies) == 2
    #     assert movies == movie_dao_mock.get_all_movies.return_value
    #
    # def test_del_item(self, movie_dao_mock, movie_service):
    #     assert movie_service.delete_movie(id=1) is None
    #
    # def test_put_movie(self, movie_dao_mock, movie_service):
    #     assert movie_service.put_movie(id=1) is None

    def test_init(self, database):
        service = UserService()
        assert type(service.dao) == UserDAO
