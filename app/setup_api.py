from flask_restx import Api

from app.blueprints.api.api import api_blueprint

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(api_blueprint, authorizations=authorizations, security='Bearer', title='Flask Course Project 4')
