from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(
    title='Flask RESTful API',
    version='1.0',
    description='A simple REST API',
    security='Bearer Auth',
    authorizations={
        'Bearer Auth': {
            
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    }
)

