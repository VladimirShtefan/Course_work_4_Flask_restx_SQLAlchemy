from typing import List

from app.dao.base import BaseDAO
from app.dao.model.movie import Movie
from app.dao.model.user import Users, Role
from sqlalchemy.exc import IntegrityError

from app.dao.model.user_movie import UserMovie
from app.exceptions import BadRequest


class UserDAO(BaseDAO[Users]):
    __model__ = Users

    def create_user(self, email: str, password: bytes, role: Role) -> None:
        new_user = Users(email=email, password=password, role=role)
        self.db_session.add(new_user)
        try:
            self.db_session.flush()
        except IntegrityError as e:
            self.db_session.rollback()
            self.logger.info(e.orig)
            raise BadRequest(e.orig)

    def search_user(self, email: str) -> Users | None:
        return self.db_session.query(self.__model__).filter_by(email=email).first()

    def add_user_token(self, user: Users, refresh_token: str) -> None:
        user.refresh_token = refresh_token
        self.db_session.flush()

    def update_user(self, email: str, favourite_genre: str, name: str, surname: str) -> None:
        self.db_session.query(self.__model__).filter_by(email=email).update({
            'name': name,
            'surname': surname,
            'favourite_genre': favourite_genre
        })
        try:
            self.db_session.flush()
        except IntegrityError as e:
            self.db_session.rollback()
            self.logger.info(e.orig)
            raise BadRequest(e.orig)

    def change_user_password(self, email: str, hash_old_password: bytes, hash_new_password: bytes) -> None:
        user = self.db_session.query(self.__model__).filter_by(email=email).first()
        if user.password == hash_old_password:
            user.password = hash_new_password
            try:
                self.db_session.flush()
            except IntegrityError as e:
                self.db_session.rollback()
                self.logger.info(e.orig)
                raise BadRequest(e.orig)

    def add_movie_in_favorites(self, movie_id: int, email: str) -> None:
        if user_id := self.search_user(email).id:
            new_user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
            self.db_session.add(new_user_movie)
            try:
                self.db_session.flush()
            except IntegrityError as e:
                self.db_session.rollback()
                self.logger.info(e.orig)
                raise BadRequest(e.orig)

    def get_favorite_movies(self, email: str) -> List[Movie]:
        if user_id := self.search_user(email).id:
            return self.db_session.query(Movie).join(UserMovie).filter_by(user_id=user_id).all()

    def delete_movie_from_favorites(self, movie_id: int, email: str) -> None:
        user_id = self.search_user(email).id
        movie = self.db_session.query(UserMovie).filter_by(user_id=user_id, movie_id=movie_id).first()
        self.db_session.delete(movie)
