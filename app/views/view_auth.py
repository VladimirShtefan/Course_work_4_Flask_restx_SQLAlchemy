from flask_cors import cross_origin
from flask_restx import Namespace, Resource

from app.dao.model.exceptions import bad_request_model
from app.dao.model.user import token_model
from app.exceptions import TokenExpired, ValidationError, InvalidPassword
from app.service.parsers import login_parser, update_access_parser, user_parser
from app.service.user import UserService

auth_ns = Namespace('auth')


@auth_ns.route('/login/')
class AuthView(Resource):
    @auth_ns.expect(login_parser)
    @auth_ns.marshal_with(token_model, code=201, description='Tokens created')
    @auth_ns.response(code=401, description='Unauthorized')
    def post(self):
        data = login_parser.parse_args()
        tokens = UserService().search_user(**data)
        return tokens, 201

    @auth_ns.expect(update_access_parser)
    @auth_ns.marshal_with(token_model, code=201, description='Tokens created')
    @auth_ns.response(code=401, description='Unauthorized')
    def put(self):
        tokens: dict = update_access_parser.parse_args()
        try:
            return UserService().update_tokens(tokens), 201
        except TokenExpired:
            return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=invalid_refresh_token'}


@auth_ns.route('/register/')
class RegisterView(Resource):
    @auth_ns.expect(user_parser)
    @auth_ns.response(code=201, description='Created')
    @auth_ns.response(code=401, description='Unauthorized')
    @auth_ns.response(code=400, description='Bad request', model=bad_request_model)
    def post(self):
        data = user_parser.parse_args()
        try:
            UserService().create_user(**data)
        except ValidationError:
            return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=not strong password'}
        except InvalidPassword:
            return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=wrong password'}
        return None, 201
