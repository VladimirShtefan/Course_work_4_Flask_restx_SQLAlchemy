from flask_restx import Namespace, Resource

from app.dao.model.user import token_model
from app.exceptions import TokenExpired
from app.service.parsers import login_parser, update_access_parser
from app.service.user import UserService

auth_ns = Namespace('auth')


@auth_ns.route('/')
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
