import enum

from flask_restx import fields

from app.setup_api import api
from app.setup_db import db


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum(Role), default=Role.user, nullable=False)
    refresh_token = db.Column(db.String, unique=True)


user_model = api.model(
    'User',
    {
        'id': fields.Integer(required=True, example=12),
        'username': fields.String(max_length=50, required=True, example='username'),
        'password': fields.String(max_length=255, required=True, example='password'),
        'role': fields.String(enum=[x.name for x in Role], required=True, example='user or admin'),
    }
)

token_model = api.model(
    'Token',
    {
        'access_token': fields.String(max_length=255,
                                      example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJvYiIsInJvbGUiOiJ'
                                              '1c2VyIiwiZXhwIjoxNjYxMjU2NDI1fQ.C4YBaCTIdH6sgXjPvRCc79-KjI-aeJIimoUJdlqy'
                                              'Raw'),
        'refresh_token': fields.String(max_length=255,
                                       example='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJvYiIsInJvbGUiOi'
                                               'J1c2VyIiwiZXhwIjoxNjYxMjU2NDI1fQ.C4YBaCTIdH6sgXjPvRCc79-KjI-aeJIimoUJdl'
                                               'qyRaw'),
    }
)
