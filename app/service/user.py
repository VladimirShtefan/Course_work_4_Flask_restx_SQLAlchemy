import calendar
import hashlib
import re
import hmac

import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError

from app.constants import SECRET, ALGORITHMS, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from app.dao.model.user import User, Role
from app.dao.user import UserDAO
from app.exceptions import ValidationError, UserNotFound, InvalidPassword, TokenExpired
from app.service.base import BaseService


class UserService(BaseService[User]):
    def __init__(self):
        super().__init__()
        self.dao = UserDAO()

    @staticmethod
    def get_hash(password: str) -> bytes:
        hash_password = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hash_password

    @staticmethod
    def check_reliability(password: str,
                          pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$') -> str:
        if re.match(pattern, password) is None:
            raise ValidationError('Password has incorrect format.')
        return password

    @staticmethod
    def add_data_for_token(delta_for_token: dict, data: dict) -> str:
        """

        :param data: data for token
        :param delta_for_token: {'minutes': 60} {'days': 90}
        :return:
        """
        delay = datetime.utcnow() + timedelta(**delta_for_token)
        data['exp'] = calendar.timegm(delay.timetuple())
        token = jwt.encode(data, SECRET, algorithm=ALGORITHMS)
        return token

    def generate_tokens(self, data: dict) -> dict:
        access_token = self.add_data_for_token(data=data, delta_for_token={'minutes': 60})
        refresh_token = self.add_data_for_token(data=data, delta_for_token={'days': 90})
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    def search_user(self, **kwargs):
        username: str = kwargs.get('username')
        password: bytes = self.get_hash(kwargs.get('password'))
        user = self.dao.search_user(username)

        if user is None:
            raise UserNotFound(f'User with username:{username}, not found')

        if not hmac.compare_digest(user.password, password):
            raise InvalidPassword('Invalid password')
        data = {'username': user.username, 'role': user.role.name}
        tokens = self.generate_tokens(data)
        self.dao.add_user_token(user, tokens.get('refresh_token'))
        return tokens

    def create_user(self, **kwargs):
        password: bytes = self.get_hash(self.check_reliability(kwargs.get('password')))
        username: str = kwargs.get('username')
        role: str = kwargs.get('role')
        return self.dao.create_user(username, password, Role(role))

    def approve_refresh_token(self, refresh_token: str) -> dict:
        try:
            data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[ALGORITHMS])
        except ExpiredSignatureError:
            raise TokenExpired('Refresh token expired')
        username = data.get('username')
        role = data.get('role')
        data_for_new_token = {'username': username, 'role': role}
        tokens = self.generate_tokens(data_for_new_token)
        user = self.dao.search_user(username)
        self.dao.add_user_token(user, tokens.get('refresh_token'))
        return tokens

    def update_tokens(self, tokens: dict) -> dict:
        refresh_token = tokens.get('refresh_token')
        return self.approve_refresh_token(refresh_token)
