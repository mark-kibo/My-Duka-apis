from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest
from ..models.users import Users  

# Create a Flask web application instance
app = Flask(__name__)

# Create an SQLAlchemy database instance and associate it with the Flask app

bcrypt = Bcrypt()
api = Api(app, version='1.0', title='Your API', description='User Signup API')

# Create database tables based on defined models


# Namespace for user-related operations
signup_namespace = Namespace('signup', description='signup operations')

# Request parser for the signup endpoint, defining expected parameters
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True, help='Username is required')
signup_parser.add_argument('password', type=str, required=True, help='Password is required')
signup_parser.add_argument('email', type=str, required=True, help='Email is required')
signup_parser.add_argument('full_name', type=str, required=True, help='Full name is required')
signup_parser.add_argument('role', type=str, required=True, help='Role is required')
signup_parser.add_argument('store_id', type=int, required=True, help='Store ID is required')


def create_user(args):
    existing_user = Users.query.filter_by(username=args['username']).first()
    if existing_user:
        raise BadRequest('Username already exists')

    existing_email = Users.query.filter_by(email=args['email']).first()
    if existing_email:
        raise BadRequest('Email already exists')

    new_user = Users(
        username=args['username'],
        email=args['email'],
        full_name=args['full_name'],
        role=args['role'],
        store_id=args['store_id']
    )
    new_user.set_password(args['password'])
    new_user.save()


@signup_namespace.route('/signup')
class SignupResource(Resource):
    @api.expect(signup_parser)
    def post(self):
        try:
            args = signup_parser.parse_args()
            create_user(args)
            return {'message': 'User created successfully'}, 201
        except BadRequest as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500




# Run the Flask application if executed as the main script
if __name__ == '__main__':
    app.run(debug=True)
