import calendar
import hashlib
import re
import hmac
from typing import List

import jwt
from datetime import datetime, timedelta
from jwt.exceptions import ExpiredSignatureError

from app.constants import SECRET, ALGORITHMS, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from app.dao.model.movie import Movie
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

    def search_user(self, **kwargs) -> dict:
        email: str = kwargs.get('email')
        password: bytes = self.get_hash(kwargs.get('password'))
        user = self.dao.search_user(email)

        if user is None:
            raise UserNotFound(f'User with email:{email}, not found')

        if not hmac.compare_digest(user.password, password):
            raise InvalidPassword('Invalid password')
        data = {'email': user.email, 'role': user.role.name}
        tokens = self.generate_tokens(data)
        self.dao.add_user_token(user, tokens.get('refresh_token'))
        return tokens

    def create_user(self, **kwargs) -> None:
        password: bytes = self.get_hash(self.check_reliability(kwargs.get('password')))
        email: str = kwargs.get('email')
        role: str = kwargs.get('role')
        if role in list(map(str, Role)):
            user_role = Role(role)
        else:
            user_role: Role = Role.user
        return self.dao.create_user(email, password, user_role)

    def approve_refresh_token(self, refresh_token: str) -> dict:
        try:
            data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[ALGORITHMS])
        except ExpiredSignatureError:
            raise TokenExpired('Refresh token expired')
        email = data.get('email')
        role = data.get('role')
        data_for_new_token = {'email': email, 'role': role}
        tokens = self.generate_tokens(data_for_new_token)
        user = self.dao.search_user(email)
        self.dao.add_user_token(user, tokens.get('refresh_token'))
        return tokens

    def update_tokens(self, tokens: dict) -> dict:
        refresh_token = tokens.get('refresh_token')
        return self.approve_refresh_token(refresh_token)

    def get_user_profile(self, email: str) -> User | None:
        return self.dao.search_user(email)

    def patch_user_info(self, email: str, **kwargs) -> None:
        favourite_genre = kwargs.get('favourite_genre')
        name = kwargs.get('name')
        surname = kwargs.get('surname')
        return self.dao.update_user(email, favourite_genre, name, surname)

    def change_user_password(self, email: str, **passwords) -> None:
        old_password = passwords.get('old_password')
        new_password = passwords.get('new_password')
        hash_new_password = self.get_hash(self.check_reliability(new_password))
        hash_old_password = self.get_hash(old_password)
        return self.dao.change_user_password(email, hash_old_password, hash_new_password)

    def add_movie_in_favorites(self, movie_id: int, email: str) -> None:
        return self.dao.add_movie_in_favorites(movie_id, email)

    def get_favorite_movies(self, email: str) -> List[Movie]:
        return self.dao.get_favorite_movies(email)

    def delete_movie_from_favorites(self, movie_id: int, email: str) -> None:
        return self.dao.delete_movie_from_favorites(movie_id, email)
