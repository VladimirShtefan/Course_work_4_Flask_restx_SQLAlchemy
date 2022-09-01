from app.dao.genre import GenreDAO
from app.dao.model.genre import Genre
from app.service.base import BaseService


class GenreService(BaseService[Genre]):
    def __init__(self):
        super().__init__()
        self.dao = GenreDAO()

    def put_genre(self, gid: int, **kwargs) -> None:
        return self.dao.put_genre(gid, **kwargs)

    def add_genre(self, **kwargs) -> Genre:
        return self.dao.add_genre(**kwargs)
