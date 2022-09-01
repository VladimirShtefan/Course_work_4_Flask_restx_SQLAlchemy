import pytest

from werkzeug.exceptions import NotFound

from app.dao.model.genre import Genre
from app.exceptions import BadRequest


def test_get_one_genre_success(genre_dao, create_models):
    genre = create_models(name_model=Genre, number_of_models=1, genre_name='test_genre')
    _genre = genre_dao.get_one_by_id(genre[0].id)
    assert _genre.id == 1
    assert _genre.genre_name == 'test_genre_1'


def test_get_one_genre_not_exists(genre_dao):
    with pytest.raises(NotFound, match='Id not found'):
        genre_dao.get_one_by_id(999)


def test_get_all_genres(genre_dao, create_models):
    genre = create_models(name_model=Genre, number_of_models=2, genre_name='test_genre')
    genres = genre_dao.get_all_items()
    assert isinstance(genres, list)
    assert len(genres) == 2
    assert genres == genre


def test_add_genre_success(genre_dao, create_models):
    create_models(name_model=Genre, number_of_models=2, genre_name='test_genre')
    new_genre = genre_dao.add_genre(name='test_genre_3')
    assert isinstance(new_genre, Genre)
    assert new_genre.id == 3
    assert new_genre.genre_name == 'test_genre_3'


def test_add_genre_exception(genre_dao, create_models):
    create_models(name_model=Genre, number_of_models=2, genre_name='test_genre')
    with pytest.raises(BadRequest):
        genre_dao.add_genre(name='test_genre_1')


def test_put_genre_success(genre_dao, create_models, database):
    create_models(name_model=Genre, number_of_models=1, genre_name='test_genre')
    genre_dao.put_genre(1, name='put_test_genre')
    new_genre = database.session.query(Genre).get(1)
    assert isinstance(new_genre, Genre)
    assert new_genre.id == 1
    assert new_genre.genre_name == 'put_test_genre'


def test_put_genre_exception(genre_dao, create_models):
    create_models(name_model=Genre, number_of_models=2, genre_name='test_genre')
    with pytest.raises(BadRequest):
        assert genre_dao.put_genre(2, name='test_genre_1')


def test_delete_genre_success(genre_dao, create_models, database):
    create_models(name_model=Genre, number_of_models=2, genre_name='test_genre')
    all_genres = database.session.query(Genre).all()
    genre_dao.delete_row(1)
    genres_after_delete = database.session.query(Genre).all()
    assert len(all_genres) - 1 == len(genres_after_delete)


def test_delete_genre_exception(genre_dao):
    with pytest.raises(NotFound):
        genre_dao.delete_row(999)
