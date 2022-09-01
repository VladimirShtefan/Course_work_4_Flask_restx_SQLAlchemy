from typing import TypeVar, Generic, List, Optional
from flask import g
from sqlalchemy.orm.scoping import scoped_session

from app.setup_db import db
from logger import create_logger

T = TypeVar('T', bound=db.Model)


class BaseDAO(Generic[T]):
    __model__ = db.Model

    def __init__(self, db_session: Optional[scoped_session] = None):
        self.db_session = getattr(g, 'session', db_session)
        self.logger = create_logger(self.__class__.__name__)

    def get_one_by_id(self, id: int) -> T:
        return self.db_session.query(self.__model__).get_or_404(id, description='Id not found')

    def delete_row(self, id: int) -> None:
        model = self.db_session.query(self.__model__).get_or_404(id, description='Id not found')
        self.db_session.delete(model)

    def get_all_items(self) -> List[T]:
        return self.db_session.query(self.__model__).all()
