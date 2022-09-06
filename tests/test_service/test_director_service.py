from unittest.mock import patch
from werkzeug.exceptions import NotFound

import pytest

from app.dao.director import DirectorDAO
from app.dao.model.director import Director
from app.service.director import DirectorService


class TestDirectorService:
    @pytest.fixture()
    @patch('app.dao.director.DirectorDAO')
    def director_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_one_by_id.return_value = Director(id=1, name='test_director')
        dao.get_all_items.return_value = [
            Director(id=1, name='test_director_1'),
            Director(id=2, name='test_director_2'),
        ]
        dao.add_director.return_value = [
            Director(id=1, name='test_director_1'),
            Director(id=2, name='test_director_2'),
        ]
        dao.delete_row.return_value = None
        dao.put_director.return_value = None
        return dao

    @pytest.fixture()
    def director_service(self, director_dao_mock):
        with patch.object(DirectorService, '__init__', lambda self: None):
            director = DirectorService()
            director.dao = director_dao_mock
            yield director

    @pytest.fixture
    def director(self, database):
        obj = Director(name="test_director_1")
        database.session.add(obj)
        database.session.commit()
        return obj

    def test_get_director(self, director_service, director):
        assert director_service.get_item_by_id(director.id)

    def test_director_not_found(self, director_dao_mock, director_service):
        director_dao_mock.get_one_by_id.side_effect = NotFound
        with pytest.raises(NotFound):
            director_service.get_item_by_id(10)

    def test_add_director(self, director_dao_mock, director_service, director):
        new_director = director_service.add_director()
        assert new_director[1].id == 2

    @pytest.mark.parametrize('page', [1, None])
    def test_get_directors(self, director_dao_mock, director_service, page):
        directors = director_service.get_all_items(page=page)
        assert len(directors) == 2
        assert directors == director_dao_mock.get_all_items.return_value
        director_dao_mock.get_all_items.assert_called_with(page=page)

    def test_del_item(self, director_dao_mock, director_service):
        assert director_service.del_item(id=1) is None

    def test_put_director(self, director_dao_mock, director_service):
        assert director_service.put_director(did=1) is None

    def test_init(self, database):
        service = DirectorService()
        assert type(service.dao) == DirectorDAO
