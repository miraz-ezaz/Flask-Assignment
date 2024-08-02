from .extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import jwt
from flask import current_app

class UserRole(enum.Enum):
    ADMIN = "Admin"
    USER = "User"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role.value,
            'create_date': self.create_date,
            'update_date': self.update_date,
            'active': self.active
        }

    def generate_reset_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(user_id)
