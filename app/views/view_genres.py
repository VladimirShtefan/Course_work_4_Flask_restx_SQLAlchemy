from flask_restx import Namespace, Resource
from flask import url_for

from app.dao.model.exceptions import not_found_model, bad_request_model
from app.dao.model.genre import genre_model
from app.dao.model.user import Role
from app.helpers.decorators import user_required
from app.service.genre import GenreService
from app.service.parsers import name_model_parser, page_parser

genre_ns = Namespace('genres')


@genre_ns.route('/')
@genre_ns.response(code=401, description='Unauthorized')
@genre_ns.response(code=403, description='Forbidden')
class GenresView(Resource):
    @user_required(Role.user, Role.admin)
    @genre_ns.expect(page_parser)
    @genre_ns.marshal_list_with(genre_model, code=200)
    def get(self, email: str = None):
        page = page_parser.parse_args()
        return GenreService().get_all_items(**page), 200

    @user_required(Role.admin)
    @genre_ns.expect(name_model_parser)
    @genre_ns.marshal_list_with(genre_model, code=201, description='Created')
    @genre_ns.response(code=400, description='Bad request', model=bad_request_model)
    def post(self, email: str = None):
        data = name_model_parser.parse_args()
        request = GenreService().add_genre(**data)
        return request, 201, {'Location': url_for('genres_genre_view', id=request.id)}


@genre_ns.route('/<int:id>/')
@genre_ns.response(code=401, description='Unauthorized')
@genre_ns.response(code=403, description='Forbidden')
class GenreView(Resource):
    @user_required(Role.user, Role.admin)
    @genre_ns.marshal_with(genre_model, code=200)
    @genre_ns.response(code=404, description='Id not found', model=not_found_model)
    def get(self, id: int, email: str = None):
        return GenreService().get_item_by_id(id), 200

    @user_required(Role.admin)
    @genre_ns.expect(name_model_parser)
    @genre_ns.response(code=204, description='Updated')
    @genre_ns.response(code=404, description='Id not found', model=not_found_model)
    @genre_ns.response(code=400, description='Bad request', model=bad_request_model)
    def put(self, id: int, email: str = None):
        data = name_model_parser.parse_args()
        GenreService().put_genre(id, **data)
        return None, 204

    @user_required(Role.admin)
    @genre_ns.response(code=204, description='Deleted')
    @genre_ns.response(code=404, description='Id not found', model=not_found_model)
    def delete(self, id: int, email: str = None):
        GenreService().del_item(id)
        return None, 204
