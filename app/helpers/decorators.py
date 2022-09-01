import jwt
from jwt.exceptions import PyJWTError
from flask import request
from functools import wraps
from typing import Callable

from app.constants import SECRET, ALGORITHMS
from app.dao.model.user import Role


def user_required(*user_role):
    def auth_required(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=Access denied'}

            data = request.headers['Authorization']
            token = data.split('Bearer ')[-1]

            try:
                data_token = jwt.decode(token, SECRET, algorithms=[ALGORITHMS])
            except PyJWTError:
                return {'error': 'Auth-required'}, 401, {'WWW-Authenticate': 'Bearer error=Access denied'}
            else:
                role = Role(data_token.get('role', 'user'))
                username = data_token['username']

                if role not in user_role:
                    return {'error': 'Auth-required'}, 403, \
                           {'WWW-Authenticate': f'Bearer error=Access denied for {username}'}

                return func(*args, **kwargs, username=data_token['username'])

        return wrapper

    return auth_required
