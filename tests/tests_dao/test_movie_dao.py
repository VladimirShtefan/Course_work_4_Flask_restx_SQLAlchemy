import pytest

from app.exceptions import BadRequest


def test_get_director_and_genre_id(create_models, genre_dao, director_dao, movie_dao):
    director = create_models(name_model=director_dao.__model__, number_of_models=1, name='test_director')
    genre = create_models(name_model=genre_dao.__model__, number_of_models=1, name='test_genre')
    assert movie_dao.get_director_and_genre_id('test_genre_1', 'test_director_1') == (director[0].id, genre[0].id)
    assert movie_dao.get_director_and_genre_id('test_genre_999', 'test_director_1') == (director[0].id, genre[0].id + 1)
    assert movie_dao.get_director_and_genre_id('test_genre_1', 'test_director_999') == (director[0].id + 1, genre[0].id)


def test_get_all_movies(create_models, movie_dao):
    movie = create_models(name_model=movie_dao.__model__, number_of_models=2,
                          title='title')
    movies = movie_dao.get_all_movies()
    assert isinstance(movies, list)
    assert len(movies) == 2
    assert movies == movie


def test_get_filter_movies_by_movie(create_models, movie_dao):
    movie = create_models(name_model=movie_dao.__model__, number_of_models=3,
                          title='title')
    movies_with_args = movie_dao.get_all_movies(title='title_3')
    assert isinstance(movies_with_args, list)
    assert len(movies_with_args) == 1
    assert movies_with_args == [movie[2]]


def test_get_all_order_movies(create_models, movie_dao):
    movies = create_models(name_model=movie_dao.__model__, number_of_models=3,
                           title='title', year=2010)
    order_movies = movie_dao.get_all_movies(status='new')
    assert isinstance(order_movies, list)
    assert len(order_movies) == 3
    assert order_movies[0] == movies[2]


def test_paginate_movies(create_models, movie_dao):
    create_models(name_model=movie_dao.__model__, number_of_models=15,
                  title='title', year=2010)
    paginate_movies = movie_dao.get_all_movies(page=1)
    assert isinstance(paginate_movies, list)
    assert len(paginate_movies) == 12
    paginate_movies = movie_dao.get_all_movies(page=2)
    assert isinstance(paginate_movies, list)
    assert len(paginate_movies) == 3
    assert movie_dao.get_all_movies(page=12) == []


def test_add_movie(movie_dao, genre_dao, director_dao):
    new_movie = movie_dao.add_movie(title='title', genre_name='genre_name', director_name='director_name')
    assert new_movie.id == 1
    assert new_movie.title == 'title'
    assert new_movie.genre_id == 1
    assert new_movie.director_id == 1


def test_add_movie_bad_request(movie_dao):
    with pytest.raises(BadRequest):
        movie_dao.add_movie(genre_name='genre_name', director_name='director_name')
    with pytest.raises(BadRequest):
        movie_dao.add_movie()


def test_put_movie_bad_request(create_models, movie_dao):
    create_models(name_model=movie_dao.__model__, number_of_models=1,
                  title='title', year=2010)
    with pytest.raises(BadRequest):
        movie_dao.put_movie(1)
    movie = movie_dao.put_movie(1, genre_name='genre_name', director_name='director_name')
    assert movie == ''
    with pytest.raises(BadRequest):
        movie_dao.put_movie(1, test='test', genre_name='genre_name', director_name='director_name')
