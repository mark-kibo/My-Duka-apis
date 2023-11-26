from flask import Flask, url_for
from flask_mail import Message
from flask_restx import Namespace, Resource, fields, reqparse
from itsdangerous import URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest
from api.models.users import Users
from ..utils import mail


signup_ns = Namespace('signup', description='User Signup API')

signup_model = signup_ns.model('Signup', {
    'username': fields.String(required=True, description='Username is required'),
    'password': fields.String(required=True, description='Password is required'),
    'email': fields.String(required=True, description='Email is required'),
    'full_name': fields.String(required=True, description='Full name is required'),
    'role': fields.String(required=True, description='Role is required'),
    'store_id': fields.Integer(required=True, description='Store ID is required')
})

serializer = URLSafeTimedSerializer('sign')

# Define the Flask-RESTx model for email
email_model = signup_ns.model('Email', {
    'link': fields.String
})

@signup_ns.route('/signup')
class SignupResource(Resource):
    def post(self):
        try:
            args = signup_ns.json

            existing_user = Users.query.filter_by(username=args['username']).first()
            if existing_user:
                raise BadRequest('Username already exists')

            existing_email = Users.query.filter_by(email=args['email']).first()
            if existing_email:
                raise BadRequest('Email already exists')

            # Directly pass values to Message constructor
            msg = Message("Confirm Your Registration",
                          sender='your_default_sender@example.com',
                          recipients=[args['email']])

            confirmation_link = url_for('signup.confirm_registration', token=serializer.dumps(args['email'], salt='email-confirm', max_age=3600), _external=True)

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
            args = signup_ns.json
            
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
            
            if email:
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
                
                return {'message': 'User registered successfully'}, 200
            else:
                return {'error': 'Token expired or invalid'}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500


