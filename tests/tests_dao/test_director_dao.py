import pytest
from werkzeug.exceptions import NotFound

from app.exceptions import BadRequest


def test_get_one_director_success(director_dao, create_models):
    director = create_models(name_model=director_dao.__model__, number_of_models=1, director_name='test_director')
    _director = director_dao.get_one_by_id(director[0].id)
    assert _director.id == 1
    assert _director.director_name == 'test_director_1'


def test_get_one_director_not_exists(director_dao):
    with pytest.raises(NotFound, match='Id not found'):
        director_dao.get_one_by_id(999)


def test_get_all_director(director_dao, create_models):
    director = create_models(name_model=director_dao.__model__, number_of_models=2, director_name='test_director')
    directors = director_dao.get_all_items()
    assert isinstance(directors, list)
    assert len(directors) == 2
    assert directors == director


def test_add_director_success(director_dao, create_models):
    create_models(name_model=director_dao.__model__, number_of_models=2, director_name='test_director')
    new_director = director_dao.add_director(name='test_director_3')
    assert isinstance(new_director, director_dao.__model__)
    assert new_director.id == 3
    assert new_director.director_name == 'test_director_3'


def test_add_director_exception(director_dao, create_models):
    create_models(name_model=director_dao.__model__, number_of_models=2, director_name='test_director')
    with pytest.raises(BadRequest):
        director_dao.add_director(name='test_director_1')


def test_put_director_success(director_dao, create_models, database):
    create_models(name_model=director_dao.__model__, number_of_models=1, director_name='test_director')
    director_dao.put_director(1, name='put_test_director')
    new_director = database.session.query(director_dao.__model__).get(1)
    assert isinstance(new_director, director_dao.__model__)
    assert new_director.id == 1
    assert new_director.director_name == 'put_test_director'


def test_put_director_exception(director_dao, create_models):
    create_models(name_model=director_dao.__model__, number_of_models=2, director_name='test_director')
    with pytest.raises(BadRequest):
        assert director_dao.put_director(2, name='test_director_1')


def test_delete_director_success(director_dao, create_models, database):
    create_models(name_model=director_dao.__model__, number_of_models=2, director_name='test_director')
    all_directors = database.session.query(director_dao.__model__).all()
    director_dao.delete_row(1)
    directors_after_delete = database.session.query(director_dao.__model__).all()
    assert len(all_directors) - 1 == len(directors_after_delete)


def test_delete_director_exception(director_dao):
    with pytest.raises(NotFound):
        director_dao.delete_row(999)
