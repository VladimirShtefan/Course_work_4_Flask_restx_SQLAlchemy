from flask_restx import Namespace, Resource

from app.dao.model.exceptions import bad_request_model
from app.dao.model.movie import movie_model
from app.dao.model.user import Role
from app.helpers.decorators import user_required
from app.service.user import UserService

favorites_ns = Namespace('favorites')


@favorites_ns.route('/movies/')
@favorites_ns.response(code=401, description='Unauthorized')
@favorites_ns.response(code=403, description='Forbidden')
class FavoritesView(Resource):
    @user_required(Role.user, Role.admin)
    @favorites_ns.marshal_with(movie_model, code=200)
    def get(self, email: str = None):
        return UserService().get_favorite_movies(email), 200


@favorites_ns.route('/movies/<int:movie_id>/')
class FavoriteView(Resource):
    @user_required(Role.user, Role.admin)
    @favorites_ns.response(code=201, description='movie added to favorites')
    @favorites_ns.response(code=400, description='Bad request', model=bad_request_model)
    def post(self, movie_id: int,  email: str = None):
        return UserService().add_movie_in_favorites(movie_id, email), 201

    @user_required(Role.user, Role.admin)
    @favorites_ns.response(code=204, description='movie deleted from favorites')
    @favorites_ns.response(code=400, description='Bad request', model=bad_request_model)
    def delete(self, movie_id: int,  email: str = None):
        return UserService().delete_movie_from_favorites(movie_id, email), 204
