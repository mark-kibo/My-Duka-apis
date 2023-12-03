from flask import Flask, abort
from flask_restx import Api, Resource, fields, Namespace, reqparse
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash
from api.models.users import User 




api = Api()

signup_namespace = Namespace('signup', description='signup endpoints')

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
signup_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
signup_parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
signup_parser.add_argument('full_name', type=str, required=True, help='Full Name cannot be blank')
signup_parser.add_argument('role', type=str, required=True, help='Role cannot be blank')
signup_parser.add_argument('store_id', type=int, required=False, help='Store ID cannot be blank')

ROLES = ['merchant', 'admin', 'clerk']

signup_model = signup_namespace.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(required=True, description='Email'),
    'full_name': fields.String(required=True, description='Full Name'),
    'role': fields.String(required=True, description='Role', enum=ROLES)
})


@signup_namespace.route('/')
class SignupResource(Resource):
    @api.doc(responses={201: 'User registered successfully', 400: 'Invalid store_id or role', 409: 'Username or email already exists'})
    @api.expect(signup_model, validate=True)
    def post(self):
        """
        Register a new user.
        """
        data = signup_parser.parse_args()

        username = data['username']
        plain_password = data['password']
        email = data['email']
        full_name = data['full_name']
        role = data['role']


        if data['store_id']:
            try:
                store_id = data.get('store_id')
            except ValueError:
                return {'message': 'Invalid store_id. It must be a valid integer.'}, 400
            
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return {'message': 'Username or email already exists'}, 409

        if role not in ROLES:
            abort(400, 'Invalid role. Choose from: {}'.format(', '.join(ROLES)))
            

        hashed_password = generate_password_hash(plain_password)
        new_user = User(username=username, password=hashed_password, email=email, full_name=full_name, role=role)
        new_user.save()
        
        return {'message': 'User registered successfully'}, 201
