from flask_restx import Resource, Namespace
from flask import url_for

from app.dao.model.exceptions import bad_request_model, not_found_model
from app.dao.model.movie import movie_model
from app.dao.model.user import Role
from app.helpers.decorators import user_required
from app.service.movie import MovieService
from app.service.parsers import movie_filter_parser, movie_model_parser

movie_ns = Namespace('movies')


@movie_ns.route('/')
@movie_ns.response(code=401, description='Unauthorized')
@movie_ns.response(code=403, description='Forbidden')
class MoviesView(Resource):
    @user_required(Role.user, Role.admin)
    @movie_ns.expect(movie_filter_parser)
    @movie_ns.marshal_list_with(movie_model, code=200)
    def get(self, username: str):
        data = movie_filter_parser.parse_args()
        return MovieService().get_movies(**data), 200, {'User_name': username}

    @user_required(Role.admin)
    @movie_ns.expect(movie_model_parser)
    @movie_ns.marshal_list_with(movie_model, code=201, description='Created')
    @movie_ns.response(code=400, description='Bad request', model=bad_request_model)
    def post(self, username: str):
        data = movie_model_parser.parse_args()
        request = MovieService().add_movie(**data)
        return request, 201, {'Location': url_for('movies_movie_view', mid=request.id), 'User_name': username}


@movie_ns.route('/<int:mid>')
@movie_ns.response(code=401, description='Unauthorized')
@movie_ns.response(code=403, description='Forbidden')
class MovieView(Resource):
    @user_required(Role.user, Role.admin)
    @movie_ns.marshal_with(movie_model, code=200)
    @movie_ns.response(code=404, description='Id not found', model=not_found_model)
    def get(self, mid: int, username: str):
        return MovieService().get_movie(mid), 200, {'User_name': username}

    @user_required(Role.admin)
    @movie_ns.expect(movie_model_parser)
    @movie_ns.response(code=204, description='Updated')
    @movie_ns.response(code=400, description='Bad request', model=bad_request_model)
    def put(self, mid: int, username: str):
        data = movie_model_parser.parse_args()
        MovieService().put_movie(mid, **data)
        return "", 204, {'User_name': username}

    @user_required(Role.admin)
    @movie_ns.response(code=204, description='Deleted')
    @movie_ns.response(code=404, description='Id not found', model=not_found_model)
    def delete(self, mid: int, username: str):
        MovieService().delete_movie(mid)
        return "", 204, {'User_name': username}
