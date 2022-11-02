import enum

from flask_restx import fields

from app.dao.model.movie import movie_model
from app.setup_api import api
from app.setup_db import db


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.Enum(Role), default=Role.user, nullable=True)
    refresh_token = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, nullable=True)
    favourite_genre = db.Column(db.Integer, db.ForeignKey('genre.id'))
    movies = db.relationship("Movie", secondary='user_movie', backref='users', cascade="all, delete")


user_model = api.model(
    'Users',
    {
        'id': fields.Integer(required=True, example=12),
        'email': fields.String(max_length=50, required=True, example='email'),
        'role': fields.String(max_length=255, required=False, example='admin'),
        'name': fields.String(max_length=255, required=False, example='Bob'),
        'surname': fields.String(max_length=255, required=False, example='Shtefan'),
        'favourite_genre': fields.Integer(example=12),
        'movies': fields.Nested(movie_model),
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
