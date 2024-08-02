from flask import Flask, jsonify
from .extensions import db, migrate, jwt, api
from .routes import api as api_namespace
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

def create_app():
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Ensure the database exists
    ensure_database_exists(app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Handle JWT errors
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({
            'message': 'Missing Authorization Header'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        return jsonify({
            'message': 'Invalid Token'
        }), 422

    # Register the API namespace
    api.add_namespace(api_namespace, path='/api')
    api.init_app(app)

    return app

def ensure_database_exists(database_uri):
    engine = create_engine(database_uri)
    db_name = engine.url.database
    db_user = engine.url.username
    db_password = engine.url.password
    db_host = engine.url.host
    db_port = engine.url.port
    
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} created.")
    else:
        print(f"Database {db_name} already exists.")
    
    cur.close()
    conn.close()
