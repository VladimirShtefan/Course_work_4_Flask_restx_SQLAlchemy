from typing import List

from app.dao.model.movie import Movie
from app.dao.movie import MovieDAO
from app.service.base import BaseService


class MovieService(BaseService[Movie]):
    def __init__(self):
        super().__init__()
        self.dao = MovieDAO()

    def get_movies(self, **kwargs) -> List[Movie]:
        return self.dao.get_all_movies(**kwargs)

    def add_movie(self, **kwargs) -> Movie:
        return self.dao.add_movie(**kwargs)

    def put_movie(self, id: int, **kwargs) -> None:
        return self.dao.put_movie(id=id, **kwargs)

    def delete_movie(self, id: int) -> None:
        return self.dao.delete_row(id=id)

    def get_movie(self, id: int) -> Movie:
        return self.dao.get_one_by_id(id=id)
