# Import necessary modules from Flask and Flask extensions
from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest
from models.users import Users


# Create a Flask web application instance
app = Flask(__name__)

# Configure the SQLAlchemy extension with the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

# Create an SQLAlchemy database instance and associate it with the Flask app
db = SQLAlchemy(app)

bcrypt = Bcrypt()
api = Api()

# Create a Flask-RESTx API instance, providing version and description
api = Api(app, version='1.0', title='Your API', description='User Signup API')

# Request parser for the signup endpoint, defining expected parameters
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('username', type=str, required=True, help='Username is required')
signup_parser.add_argument('password', type=str, required=True, help='Password is required')
signup_parser.add_argument('email', type=str, required=True, help='Email is required')
signup_parser.add_argument('full_name', type=str, required=True, help='Full name is required')
signup_parser.add_argument('role', type=str, required=True, help='Role is required')
signup_parser.add_argument('store_id', type=int, required=True, help='Store ID is required')

# Define a resource for the signup endpoint using Flask-RESTx
@api.route('/signup')
class SignupResource(Resource):
    @api.expect(signup_parser)
    def post(self):
        try:
            # Parse the request arguments
            args = signup_parser.parse_args()

            # Check if the username or email already exists
            existing_user = Users.query.filter_by(username=args['username']).first()
            if existing_user:
                raise BadRequest('Username already exists')

            existing_email = Users.query.filter_by(email=args['email']).first()
            if existing_email:
                raise BadRequest('Email already exists')

            # Create a new Users instance with the parsed arguments
            new_user = Users(
                username=args['username'],
                email=args['email'],
                full_name=args['full_name'],
                role=args['role'],
                store_id=args['store_id']
            )

            # Use the set_password method to hash the password
            new_user.set_password(args['password'])

            # Save the new user to the database
            new_user.save()
            return {'message': 'User created successfully'}, 201

        except BadRequest as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

# Run the Flask application if executed as the main script
if __name__ == '__main__':
    app.run(debug=True)
