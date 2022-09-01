from typing import List
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app.dao.base import BaseDAO
from app.dao.model.director import Director
from app.dao.model.genre import Genre
from app.dao.model.movie import Movie
from app.exceptions import BadRequest


class MovieDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_director_and_genre_id(self, genre_name: str, director_name: str) -> tuple[int, int]:
        director = self.db_session.query(Director).filter(Director.director_name.ilike(director_name)).first()
        genre = self.db_session.query(Genre).filter(Genre.genre_name.ilike(genre_name)).first()
        if not director:
            director_model = Director(director_name=director_name)
            self.db_session.add(director_model)
            self.db_session.flush()
            director_id = director_model.id
        else:
            director_id = director.id
        if not genre:
            genre_model = Genre(genre_name=genre_name)
            self.db_session.add(genre_model)
            self.db_session.flush()
            genre_id = genre_model.id
        else:
            genre_id = genre.id
        return director_id, genre_id

    def get_all_movies(self, **kwargs) -> List[Movie]:
        movie_query = self.db_session.query(self.__model__)
        for key, item in kwargs.items():
            if hasattr(Director, key):
                if type(item) == str:
                    movie_query = movie_query.join(Director).filter(getattr(Director, key).ilike(f'%{item}%'))
            if hasattr(Genre, key):
                if type(item) == str:
                    movie_query = movie_query.join(Genre).filter(getattr(Genre, key).ilike(f'%{item}%'))
            if hasattr(self.__model__, key):
                movie_query = movie_query.filter(getattr(self.__model__, key) == item)
        return movie_query.all()

    def add_movie(self, **kwargs) -> Movie:
        genre_name = kwargs.pop('genre_name')
        director_name = kwargs.pop('director_name')
        if director_name and genre_name:
            director_id, genre_id = self.get_director_and_genre_id(genre_name=genre_name, director_name=director_name)
            data = {'director_id': director_id, 'genre_id': genre_id}
            data.update(kwargs)

            new_movie = self.__model__(**data)

            self.db_session.add(new_movie)
            try:
                self.db_session.flush()
            except IntegrityError as e:
                self.db_session.rollback()
                self.logger.info(e.orig)
                raise BadRequest(e.orig)
            else:
                return new_movie
        raise BadRequest('Attribute error. genre_name or director_name is None')

    def put_movie(self, id: int, **kwargs):
        genre_name = kwargs.pop('genre_name')
        director_name = kwargs.pop('director_name')
        if director_name and genre_name:
            director_id, genre_id = self.get_director_and_genre_id(genre_name=genre_name, director_name=director_name)
            data = {'director_id': director_id, 'genre_id': genre_id}
            data.update(kwargs)
            try:
                self.db_session.query(self.__model__).filter_by(id=id).update(data)
            except IntegrityError as e:
                self.db_session.rollback()
                self.logger.info(e.orig)
                raise BadRequest(e.orig)
            except InvalidRequestError as e:
                self.db_session.rollback()
                self.logger.info(e.args[0])
                raise BadRequest(e.args[0])
            else:
                return ""
        raise BadRequest('Attribute error. genre_name or director_name is None')
