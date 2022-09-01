from flask_restx.reqparse import RequestParser

from app.dao.model.user import Role

movie_filter_parser: RequestParser = RequestParser()
movie_filter_parser.add_argument('director_name', type=str, location='args', store_missing=False)
movie_filter_parser.add_argument('genre_name', type=str, location='args', store_missing=False)
movie_filter_parser.add_argument('director_id', type=int, location='args', store_missing=False)
movie_filter_parser.add_argument('genre_id', type=int, location='args', store_missing=False)
movie_filter_parser.add_argument('year', type=int, location='args', store_missing=False)

movie_model_parser: RequestParser = RequestParser()
movie_model_parser.add_argument('title', location='json', type=str, required=True, nullable=False)
movie_model_parser.add_argument('description', location='json', type=str, required=False, nullable=True)
movie_model_parser.add_argument('trailer', location='json', type=str, required=False, nullable=True)
movie_model_parser.add_argument('year', location='json', type=int, required=False, nullable=True)
movie_model_parser.add_argument('rating', location='json', type=float, required=False, nullable=True)
movie_model_parser.add_argument('genre_name', location='json', type=str, required=False, nullable=True)
movie_model_parser.add_argument('director_name', location='json', type=str, required=False, nullable=True)

name_model_parser: RequestParser = RequestParser()
name_model_parser.add_argument('name', location='json', type=str, required=True, nullable=False)

user_parser: RequestParser = RequestParser()
user_parser.add_argument('username', location='json', type=str, required=True, nullable=False)
user_parser.add_argument('password', location='json', type=str, required=True, nullable=False)
user_parser.add_argument('role', default='user', choices=[x.name for x in Role],
                         location='json', type=str, required=True, nullable=False)

access_parser: RequestParser = RequestParser()
access_parser.add_argument('access_token', location='json', type=str, required=True, nullable=False)
access_parser.add_argument('refresh_token', location='json', type=str, required=True, nullable=False)

update_access_parser: RequestParser = RequestParser()
update_access_parser.add_argument('refresh_token', location='json', type=str, required=True, nullable=False)

login_parser: RequestParser = RequestParser()
login_parser.add_argument('username', location='json', type=str, required=True, nullable=False)
login_parser.add_argument('password', location='json', type=str, required=True, nullable=False)
