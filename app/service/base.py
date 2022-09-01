from typing import Generic, TypeVar, List

from app.dao.base import BaseDAO
from app.setup_db import db

TS = TypeVar('TS', bound=db.Model)


class BaseService(Generic[TS]):
    def __init__(self):
        self.dao = BaseDAO()

    def del_item(self, id: int):
        return self.dao.delete_row(id)

    def get_item_by_id(self, id: int) -> TS:
        return self.dao.get_one_by_id(id)

    def get_all_items(self) -> List[TS]:
        return self.dao.get_all_items()
