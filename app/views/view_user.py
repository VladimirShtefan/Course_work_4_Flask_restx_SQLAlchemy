from flask_restx import Namespace, Resource

from app.dao.model.exceptions import bad_request_model
from app.dao.model.user import user_model
from app.exceptions import ValidationError, InvalidPassword
from app.service.parsers import user_parser
from app.service.user import UserService

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @user_ns.expect(user_parser)
    @user_ns.response(code=201, description='Created')
    @user_ns.response(code=401, description='Unauthorized')
    @user_ns.response(code=400, description='Bad request', model=bad_request_model)
    def post(self):
        data = user_parser.parse_args()
        try:
            UserService().create_user(**data)
        except ValidationError:
            return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=not strong password'}
        except InvalidPassword:
            return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=wrong password'}
        return "", 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @user_ns.marshal_with(user_model, code=200)
    def get(self, uid: int):
        return UserService().get_item_by_id(uid)

