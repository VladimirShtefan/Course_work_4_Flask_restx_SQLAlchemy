from flask_restx import Namespace, Resource
from flask import url_for

from app.dao.model.director import director_model
from app.dao.model.exceptions import not_found_model, bad_request_model
from app.helpers.decorators import user_required
from app.service.director import DirectorService
from app.service.parsers import name_model_parser

director_ns = Namespace('directors')


@director_ns.route('/')
@director_ns.response(code=401, description='Unauthorized')
@director_ns.response(code=403, description='Forbidden')
class DirectorsView(Resource):
    @user_required(('user', 'admin'))
    @director_ns.marshal_list_with(director_model, code=200)
    def get(self, username: str):
        return DirectorService().get_all_items(), 200, {'User_name': username}

    @user_required(tuple('admin'))
    @director_ns.expect(name_model_parser)
    @director_ns.marshal_list_with(director_model, code=201, description='Created')
    @director_ns.response(code=400, description='Bad request', model=bad_request_model)
    def post(self, username: str):
        data = name_model_parser.parse_args()
        request = DirectorService().add_director(**data)
        return request, 201, {'Location': url_for('directors_director_view', did=request.id), 'User_name': username}


@director_ns.route('/<int:did>')
@director_ns.response(code=401, description='Unauthorized')
@director_ns.response(code=403, description='Forbidden')
class DirectorView(Resource):
    @user_required(('user', 'admin'))
    @director_ns.marshal_with(director_model, code=200)
    @director_ns.response(code=404, description='Id not found', model=not_found_model)
    def get(self, did: int, username: str):
        return DirectorService().get_item_by_id(did), 200, {'User_name': username}

    @user_required(tuple('admin'))
    @director_ns.expect(name_model_parser)
    @director_ns.response(code=204, description='Updated')
    @director_ns.response(code=404, description='Id not found', model=not_found_model)
    @director_ns.response(code=400, description='Bad request', model=bad_request_model)
    def put(self, did: int, username: str):
        data = name_model_parser.parse_args()
        DirectorService().put_director(did, **data)
        return "", 204, {'User_name': username}

    @user_required(tuple('admin'))
    @director_ns.response(code=204, description='Deleted')
    @director_ns.response(code=404, description='Id not found', model=not_found_model)
    def delete(self, did: int, username: str):
        DirectorService().del_item(did)
        return "", 204, {'User_name': username}
