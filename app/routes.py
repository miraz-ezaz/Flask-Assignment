from flask_restx import Namespace, Resource, fields
from .models import User, db, UserRole
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Namespace('api', description='API operations')

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'username': fields.String(required=True, description='The username of the user'),
    'first_name': fields.String(required=True, description='The first name of the user'),
    'last_name': fields.String(required=True, description='The last name of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'role': fields.String(description='The role of the user', enum=UserRole._member_names_),
    'create_date': fields.DateTime(description='The date the user was created'),
    'update_date': fields.DateTime(description='The date the user was last updated'),
    'active': fields.Boolean(description='Is the user active?'),
})

register_model = api.model('Register', {
    'username': fields.String(required=True, description='The username of the user'),
    'first_name': fields.String(required=True, description='The first name of the user'),
    'last_name': fields.String(required=True, description='The last name of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
    'role': fields.String(description='The role of the user', enum=UserRole._member_names_),
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='The username of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

reset_request_model = api.model('ResetRequest', {
    'email': fields.String(required=True, description='The email of the user'),
})

reset_password_model = api.model('ResetPassword', {
    'token': fields.String(required=True, description='The reset token'),
    'password': fields.String(required=True, description='The new password'),
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = api.payload
        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            role=data.get('role', UserRole.USER),
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = api.payload
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.username)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401

@api.route('/users')
class UserList(Resource):
    @jwt_required()
    @api.marshal_list_with(user_model)
    @api.doc(security='Bearer Auth')
    def get(self):
        users = User.query.all()
        return users

@api.route('/user/<string:username>')
@api.response(404, 'User not found')
class UserDetail(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self, username):
        current_user = get_jwt_identity()
        if current_user != username:
            return {"message": "Unauthorized access"}, 403
        
        user = User.query.filter_by(username=username).first_or_404()
        return user.to_dict()

    @jwt_required()
    @api.expect(user_model)
    @api.doc(security='Bearer Auth')
    def put(self, username):
        current_user = get_jwt_identity()
        if current_user != username:
            return {"message": "Unauthorized access"}, 403

        user = User.query.filter_by(username=username).first_or_404()
        data = api.payload
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.active = data.get('active', user.active)
        db.session.commit()
        return {"message": "User updated successfully"}, 200

    @jwt_required()
    @api.doc(security='Bearer Auth')
    def delete(self, username):
        current_user = get_jwt_identity()
        if current_user != username:
            return {"message": "Unauthorized access"}, 403

        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

@api.route('/admin/user/<string:username>')
@api.response(404, 'User not found')
class AdminUserDetail(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self, username):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if user.role != UserRole.ADMIN and current_user != username:
            return {"message": "Unauthorized access"}, 403
        
        target_user = User.query.filter_by(username=username).first_or_404()
        return target_user.to_dict()

    @jwt_required()
    @api.expect(user_model)
    @api.doc(security='Bearer Auth')
    def put(self, username):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if user.role != UserRole.ADMIN and current_user != username:
            return {"message": "Unauthorized access"}, 403

        target_user = User.query.filter_by(username=username).first_or_404()
        data = api.payload
        target_user.first_name = data.get('first_name', target_user.first_name)
        target_user.last_name = data.get('last_name', target_user.last_name)
        target_user.email = data.get('email', target_user.email)
        target_user.active = data.get('active', target_user.active)
        db.session.commit()
        return {"message": "User updated successfully"}, 200

    @jwt_required()
    @api.doc(security='Bearer Auth')
    def delete(self, username):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if user.role != UserRole.ADMIN and current_user != username:
            return {"message": "Unauthorized access"}, 403

        target_user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(target_user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

@api.route('/reset_password_request')
class ResetPasswordRequest(Resource):
    @api.expect(reset_request_model)
    def post(self):
        data = api.payload
        user = User.query.filter_by(email=data['email']).first()
        if user:
            token = user.generate_reset_token()
            print(f"Password reset token for {user.email}: {token}")
        else:
            print(f"No user found with email: {data['email']}")
        return {"message": "If your email is registered, you will receive a password reset token shortly."}, 200

@api.route('/reset_password/<token>')
class ResetPassword(Resource):
    @api.expect(reset_password_model)
    def post(self, token):
        user = User.verify_reset_token(token)
        if not user:
            return {"message": "Invalid or expired token."}, 400
        data = api.payload
        user.set_password(data['password'])
        db.session.commit()
        return {"message": "Your password has been reset successfully."}, 200
