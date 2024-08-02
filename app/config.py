import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://default_user:default_password@localhost/default_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_MASK_SWAGGER = False
    ERROR_404_HELP = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
