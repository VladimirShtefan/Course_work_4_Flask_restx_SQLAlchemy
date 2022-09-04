from flask import Flask, g
from sqlalchemy.exc import DBAPIError
from flask_cors import CORS

from app.exceptions import BaseAppException
from app.setup_api import api
from app.setup_db import db
from app.views.view_directors import director_ns
from app.views.view_favorites import favorites_ns
from app.views.view_genres import genre_ns
from app.views.view_movies import movie_ns
from app.views.view_auth import auth_ns
from app.views.view_user import user_ns
from logger import create_logger

logger = create_logger(__name__)


def create_app(config_object) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config_object)
    register_extensions(application)
    logger.info('app created')

    @application.before_request
    def open_session():
        g.session = db.session

    @application.after_request
    def close_session(response):
        if getattr(g, 'session'):
            try:
                g.session.commit()
            except DBAPIError as e:
                logger.debug(e)
                g.session.rollback()
            finally:
                g.session.close()
        return response

    return application


def register_extensions(app: Flask):
    CORS(app=app)
    db.init_app(app)
    api.init_app(app)
    api.add_namespace(movie_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(favorites_ns)

    @api.errorhandler(BaseAppException)
    def get_exception(e: BaseAppException):
        return {
                   'error': str(e.message),
                   'code': e.code
               }, e.code
