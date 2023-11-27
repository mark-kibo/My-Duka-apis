from flask import Flask, abort
from flask_restx import Api, Resource, fields, Namespace, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest
from api.models.users import User 


app = Flask(__name__)



bcrypt = Bcrypt()
api = Api(app, version='1.0', title='Your API', description='User Signup API')


signup_namespace = Namespace('signup', description='signup operations')

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
signup_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
signup_parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
signup_parser.add_argument('full_name', type=str, required=True, help='Full Name cannot be blank')
signup_parser.add_argument('role', type=str, required=True, help='Role cannot be blank')
signup_parser.add_argument('store_id', type=int, required=True, help='Store ID cannot be blank')

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
    def post(self):
        data = signup_parser.parse_args()

        username = data['username']
        plain_password = data['password']
        email = data['email']
        full_name = data['full_name']
        role = data['role']



        try:
            store_id = int(data['store_id'])
        except ValueError:
            return {'message': 'Invalid store_id. It must be a valid integer.'}, 400


        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return {'message': 'Username or email already exists'}, 409

        if role not in ROLES:
            abort(400, 'Invalid role. Choose from: {}'.format(', '.join(ROLES)))

        hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

        new_user = User(username=username, password=hashed_password, email=email, full_name=full_name, role=role)
        new_user.save()

        return {'message': 'User registered successfully'}, 201

if __name__ == '__main__':
   
    app.run(debug=True)