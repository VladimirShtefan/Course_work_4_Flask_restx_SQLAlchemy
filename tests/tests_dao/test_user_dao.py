import pytest

from app.dao.model.user import Role
from app.dao.model.user_movie import UserMovie
from app.exceptions import BadRequest


def test_create_user(user_dao, database):
    user_dao.create_user(email='email', password='password', role=Role.user)
    users = database.session.query(user_dao.__model__).all()
    assert isinstance(users, list)
    assert users[0].email == 'email'
    assert users[0].id == 1


def test_create_user_bad_request(user_dao, create_models):
    create_models(name_model=user_dao.__model__, number_of_models=1,
                  email='email', password='password')
    with pytest.raises(BadRequest):
        user_dao.create_user(email='email_1', password='password_1', role=Role.user)


def test_search_user(user_dao, create_models):
    test_user = create_models(name_model=user_dao.__model__, number_of_models=1,
                              email='email', password='password')
    user = user_dao.search_user(email='email_1')
    assert [user] == test_user


def test_add_user_token(user_dao, create_models, database):
    test_user = create_models(name_model=user_dao.__model__, number_of_models=1,
                              email='email', password='password')
    user_dao.add_user_token(test_user[0], 'token')
    users = database.session.query(user_dao.__model__).all()
    assert isinstance(users, list)
    assert users[0].refresh_token == 'token'


def test_update_user(user_dao, create_models, database):
    create_models(name_model=user_dao.__model__, number_of_models=1,
                  email='email', password='password')
    user_dao.update_user(email='email_1', name='name', favourite_genre='favourite_genre', surname='surname')
    users = database.session.query(user_dao.__model__).all()
    assert isinstance(users, list)
    assert users[0].surname == 'surname'


def test_change_user_password(user_dao, create_models, database):
    create_models(name_model=user_dao.__model__, number_of_models=1,
                  email='email', password=b'old')
    user_dao.change_user_password(email='email_1', hash_old_password=b'old', hash_new_password=b'new')
    users = database.session.query(user_dao.__model__).all()
    assert isinstance(users, list)
    assert users[0].password == b'new'


def test_add_movie_in_favorites(user_dao, create_models, database):
    create_models(name_model=user_dao.__model__, number_of_models=1,
                  email='email', password='password')
    user_dao.add_movie_in_favorites(movie_id=1, email='email_1')
    user_movie = database.session.query(UserMovie).all()
    assert isinstance(user_movie, list)
    assert user_movie[0].user_id == 1
    assert user_movie[0].movie_id == 1


def test_get_favorite_movies(user_dao, create_models, movie_dao, database):
    user_movie = UserMovie(user_id=1, movie_id=1)
    database.session.add(user_movie)
    database.session.commit()
    create_models(name_model=user_dao.__model__, number_of_models=1,
                  email='email', password='password')
    create_models(name_model=movie_dao.__model__, number_of_models=1,
                  title='title', year=2020)
    user_movies = user_dao.get_favorite_movies(email='email_1')
    assert isinstance(user_movies, list)
    assert user_movies[0].title == 'title_1'


def test_delete_movie_from_favorites(user_dao, create_models, movie_dao, database):
    user_movie_1 = UserMovie(user_id=1, movie_id=1)
    user_movie_2 = UserMovie(user_id=1, movie_id=2)
    database.session.add_all([user_movie_1, user_movie_2])
    database.session.commit()
    create_models(name_model=user_dao.__model__, number_of_models=1,
                  email='email', password='password')
    user_dao.delete_movie_from_favorites(movie_id=1, email='email_1')
    user_movie = database.session.query(UserMovie).all()
    assert user_movie[0].user_id == 1
    assert user_movie[0].movie_id == 2
