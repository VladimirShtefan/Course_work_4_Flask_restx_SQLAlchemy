from flask_restx import Namespace, Resource

from app.dao.model.exceptions import bad_request_model, not_found_model
from app.dao.model.user import user_model, Role
from app.helpers.decorators import user_required
from app.service.parsers import user_info_parser, user_passwords_parser
from app.service.user import UserService

user_ns = Namespace('user')


@user_ns.route('/')
@user_ns.response(code=401, description='Unauthorized')
@user_ns.response(code=403, description='Forbidden')
class UserView(Resource):
    @user_required(Role.user, Role.admin)
    @user_ns.marshal_with(user_model, code=200)
    @user_ns.response(code=404, description='Id not found', model=not_found_model)
    def get(self, email: str = None):
        return UserService().get_user_profile(email), 200

    @user_ns.expect(user_info_parser)
    @user_required(Role.user, Role.admin)
    @user_ns.response(code=204, description='Updated')
    @user_ns.response(code=400, description='Bad request', model=bad_request_model)
    def patch(self, email: str = None):
        data = user_info_parser.parse_args()
        return UserService().patch_user_info(email, **data), 204


@user_ns.route('/password/')
class UserPasswordView(Resource):
    @user_ns.expect(user_passwords_parser)
    @user_required(Role.user, Role.admin)
    @user_ns.response(code=204, description='Updated')
    @user_ns.response(code=400, description='Bad request', model=bad_request_model)
    def put(self, email: str = None):
        passwords = user_passwords_parser.parse_args()
        return UserService().change_user_password(email, **passwords), 204
