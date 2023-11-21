# Import necessary modules from Flask and Flask extensions
from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
# from models.users import Users  # Import the Users model if uncommented

# Create a Flask web application instance
app = Flask(__name__)

# Configure the SQLAlchemy extension with the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

# Create an SQLAlchemy database instance and associate it with the Flask app
db = SQLAlchemy(app)

# Create a Flask-RESTx API instance, providing version and description
api = Api(app, version='1.0', title='Your API', description='User Signup API')

# Define the Users model as a subclass of db.Model (SQLAlchemy base class for models)
class Users(db.Model):
    # Define columns for the Users table
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'))

    # Method to save the instance to the database
    def save(self):
        db.session.add(self)
        db.session.commit()

# Create database tables based on defined models
db.create_all()

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
    # Define a POST method for the signup endpoint
    @api.expect(signup_parser)
    def post(self):
        # Parse the request arguments
        args = signup_parser.parse_args()
        # Create a new Users instance with the parsed arguments
        new_user = Users(**args)
        # Save the new user to the database
        new_user.save()
        # Return a response indicating successful user creation
        return {'message': 'User created successfully'}, 201

# Run the Flask application if executed as the main script
if __name__ == '__main__':
    app.run(debug=True)
