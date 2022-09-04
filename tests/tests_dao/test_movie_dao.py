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
