from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app.dao.base import BaseDAO
from app.dao.model.genre import Genre
from app.exceptions import BadRequest


class GenreDAO(BaseDAO[Genre]):
    __model__ = Genre

    def put_genre(self, gid: int, **kwargs) -> None:
        genre_name = kwargs.get('name')
        try:
            self.db_session.query(self.__model__).filter_by(id=gid).update({'genre_name': genre_name})
        except (IntegrityError, InvalidRequestError) as e:
            self.db_session.rollback()
            self.logger.info(e.args[0])
            raise BadRequest(e.args[0])

    def add_genre(self, **kwargs) -> Genre:
        genre_name = kwargs.get('name')
        new_genre = self.__model__(genre_name=genre_name)
        self.db_session.add(new_genre)
        try:
            self.db_session.flush()
        except IntegrityError as e:
            self.db_session.rollback()
            self.logger.info(e.orig)
            raise BadRequest(e.orig)
        else:
            return new_genre
