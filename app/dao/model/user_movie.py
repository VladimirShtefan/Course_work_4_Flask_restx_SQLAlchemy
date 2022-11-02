from flask_restx import fields

from app.setup_api import api
from app.setup_db import db


class UserMovie(db.Model):
    __tablename__ = 'user_movie'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete="CASCADE"), primary_key=True)


favorites_model = api.model(
    'UserMovie',
    {
        'user_id': fields.Integer(required=True, example=12),
        'movie_id': fields.String(required=True, example=12),
    }
)
