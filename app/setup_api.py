from flask_restx import Api


authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(authorizations=authorizations, security='Bearer', title='Flask Course Project 4')
