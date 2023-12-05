from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from flask import current_app
from flask_bcrypt import Bcrypt
from datetime import timedelta

from ..models.users import User

bcrypt = Bcrypt()

login_namespace = Namespace('login', description='Login endpoints')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
login_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

@login_namespace.route('/merchant')
class MerchantLoginResource(Resource):
    def post(self):
        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        # Retrieve merchant user by username
        merchant = User.query.filter_by(username=username, role='merchant').first()

        if merchant:
            # Verify the password using check_password_hash
            if bcrypt.check_password_hash(merchant.password, password):
                # Generate a new access token for the merchant user
                access_token = create_access_token(identity=merchant.user_id, expires_delta=timedelta(minutes=30))
                return {'message': 'Merchant login successful', 'access_token': access_token}
            else:
                current_app.logger.warning("Invalid password for merchant: %s", username)

        return {'message': 'Invalid credentials'}, 401

@login_namespace.route('/admin')
class AdminLoginResource(Resource):
    def post(self):
        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        # Retrieve admin user by username
        admin = User.query.filter_by(username=username, role='admin').first()

        if admin:
            # Verify the password
            if check_password_hash(admin.password, password):
                access_token = create_access_token(identity=admin.user_id)
                return {'message': 'Admin login successful', 'access_token': access_token}
            else:
                current_app.logger.warning("Invalid password for admin: %s", username)

        return {'message': 'Invalid credentials'}, 401

@login_namespace.route('/clerk')
class ClerkLoginResource(Resource):
    def post(self):
        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        # Retrieve clerk user by username
        clerk = User.query.filter_by(username=username, role='clerk').first()

        if clerk:
            # Verify the password
            if check_password_hash(clerk.password, password):
                access_token = create_access_token(identity=clerk.user_id)
                return {'message': 'Clerk login successful', 'access_token': access_token}
            else:
                current_app.logger.warning("Invalid password for clerk: %s", username)

        return {'message': 'Invalid credentials'}, 401
