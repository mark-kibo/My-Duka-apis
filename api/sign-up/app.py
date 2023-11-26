from flask_restx import Namespace, Resource, fields, reqparse
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from werkzeug.exceptions import BadRequest
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from utils import mail
from models.users import Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['TOKEN_EXPIRATION'] = 600

db = SQLAlchemy(app)
bcrypt = Bcrypt()

signup_ns = Namespace('signup', description='User Signup API')

signup_model = signup_ns.model('Signup', {
    'username': fields.String(required=True, description='Username is required'),
    'password': fields.String(required=True, description='Password is required'),
    'email': fields.String(required=True, description='Email is required'),
    'full_name': fields.String(required=True, description='Full name is required'),
    'role': fields.String(required=True, description='Role is required'),
    'store_id': fields.Integer(required=True, description='Store ID is required')
})

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Define the Flask-RESTx model for email
email_model = signup_ns.model('Email', {
    'link': fields.String
})

@signup_ns.route('/signup')
class SignupResource(Resource):
    @signup_ns.expect(signup_model)
    def post(self):
        try:
            args = signup_ns.payload

            if not is_superuser():
                raise BadRequest('Only the superuser can initiate admin registration')

            existing_user = Users.query.filter_by(username=args['username']).first()
            if existing_user:
                raise BadRequest('Username already exists')

            existing_email = Users.query.filter_by(email=args['email']).first()
            if existing_email:
                raise BadRequest('Email already exists')

            token = serializer.dumps(args['email'], salt='email-confirm')

            msg = Message("Confirm Your Registration",
                          sender=app.config['MAIL_DEFAULT_SENDER'],
                          recipients=[args['email']])

            confirmation_link = url_for('confirm_registration', token=token, _external=True)

            msg.body = f"Click the following link to confirm your registration: {confirmation_link}"

            mail.send(msg)

            return {'message': 'Confirmation email sent. Check your email to complete registration.'}, 200

        except BadRequest as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

@signup_ns.route('/confirm_registration/<token>')
class ConfirmRegistration(Resource):
    def get(self, token):
        try:
            args = signup_ns.payload  # Pass args as a parameter or obtain them from the request
            
            email = serializer.loads(token, salt='email-confirm', max_age=app.config['TOKEN_EXPIRATION'])
            
            if email:
                # Email confirmed, proceed with admin registration
                # Assuming you have an Admins model
                from models.admins import Admins
                
                # Create a new Admins instance with the parsed arguments
                new_admin = Admins(
                    username=args['username'],
                    email=args['email'],
                    full_name=args['full_name'],
                    role=args['role'],
                    store_id=args['store_id']
                )
                
                # Use the set_password method to hash the password
                new_admin.set_password(args['password'])
                
                # Save the new admin to the database
                new_admin.save()
                
                return {'message': 'Admin registered successfully'}, 200
            else:
                return {'error': 'Token expired or invalid'}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

# Include the ConfirmTokenizeEmail resource in the same namespace
signup_ns.add_resource(ConfirmTokenizeEmail, '/confirm_tokenized_email/<token>')

if __name__ == '__main__':
    app.run(debug=True)
