from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app

from api.models.users import User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

login_namespace = Namespace('login', description='login endpoints')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
login_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

@login_namespace.route('/merchant')
class MerchantLoginResource(Resource):
    def post(self):
        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        merchant = User.query.filter_by(username=username, role='merchant').first()

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if merchant and bcrypt.check_password_hash(hashed_password, password):
            access_token = create_access_token(identity=merchant.user_id)
            return {'message': 'Merchant login successful', 'access_token': access_token}

        return {'message': 'Invalid credentials'}, 401

@login_namespace.route('/admin')
class AdminLoginResource(Resource):
    def post(self):
        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        admin = User.query.filter_by(username=username, role='admin').first()

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if admin and bcrypt.check_password_hash(hashed_password, password):
            access_token = create_access_token(identity=admin.user_id)
            return {'message': 'Admin login successful', 'access_token': access_token}

        return {'message': 'Invalid credentials'}, 401

@login_namespace.route('/clerk')
class ClerkLoginResource(Resource):
    def post(self):
        login_parser = reqparse.RequestParser()
        login_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
        login_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        clerk = User.query.filter_by(username=username, role='clerk').first()

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        if clerk and bcrypt.check_password_hash(hashed_password, password):
            access_token = create_access_token(identity=clerk.user_id)
            return {'message': 'Clerk login successful', 'access_token': access_token}

        return {'message': 'Invalid credentials'}, 401
