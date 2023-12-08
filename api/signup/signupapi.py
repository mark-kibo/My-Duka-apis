from flask import Flask, abort, request
from flask_restx import Api, Resource, fields, Namespace, reqparse, marshal
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash
from api.models.users import User 
from api.models.stores import Store




app = Flask(__name__)
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
    'role': fields.String(required=True, description='Role', enum=ROLES),
    'store_id': fields.Integer(required=True, description='Store ID')
})
merchant_signup_model = signup_namespace.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(required=True, description='Email'),
    'full_name': fields.String(required=True, description='Full Name'),
    'role': fields.String(required=True, description='Role', enum=ROLES)
})


@signup_namespace.route('/')
class SignupResource(Resource):
    @api.doc(responses={201: 'User registered successfully', 400: 'Invalid store_id', 409: 'Username or email already exists'})
    @api.expect(signup_model, validate=True)
    def post(self):
        """
        Register a new user (admin or clerk).
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
            
               # # Check if store_id exists in the database 
        store = Store.query.get(data['store_id'])
        if not store:
            return {"error":"store not availa"}, 404
            
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return {'message': 'Username or email already exists'}, 409

        if role not in ROLES:
            abort(400, 'Invalid role. Choose from: {}'.format(', '.join(ROLES)))
        try:


            hashed_password = generate_password_hash(plain_password)

            hashed_password = generate_password_hash(plain_password)
            new_user = User(username=username, password=hashed_password, email=email, full_name=full_name, role=role ,store_id=store_id)
            new_user.save()
            
            return marshal(new_user, signup_model), 201
        except:
            return{"error": 'Something went wrong while creating the user'}, 500
            

@signup_namespace.route('/superuser/')
class SuperuserSignupResource(Resource):
    @api.doc(responses={201: 'Superuser registered successfully', 400: 'Invalid store_id', 409: 'Username or email already exists'})
    @api.expect(merchant_signup_model, validate=True)
    def post(self):
        """
        Register a new superuser (merchant).
        """
        data = request.get_json()

        # Validate superuser-specific fields if needed

        # # Check if store_id exists in the database 
        # store = Store.query.get(data['store_id'])
        # if not store:
        #     return {"error":"store not availa"}

        existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
        if existing_user:
            return {'message': 'Username or email already exists'}, 409

        hashed_password = generate_password_hash(data['password'])


        new_user = User(username=data['username'], password=hashed_password, email=data['email'], full_name=data['full_name'], role='merchant')

        new_user.save()

        return marshal(new_user, merchant_signup_model), 201
    

@signup_namespace.route('/clerk/')
class ClerkSignupResource(Resource):
    @api.doc(responses={201: 'Clerk registered successfully', 400: 'Invalid store_id', 409: 'Username or email already exists'})
    @api.expect(signup_model, validate=True)
    def post(self):
        """
        Register a new clerk.
        """
        data = signup_parser.parse_args()

        # Validate clerk-specific fields if needed

        # Check if store_id exists in the database
        store = Store.query.get(data['store_id'])
        if not store:
            return {"error": "no store avialble with that id"}, 404

        existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
        if existing_user:
            return {'message': 'Username or email already exists'}, 409

        hashed_password = generate_password_hash(data['password'])

        new_user = User(username=data['username'], password=hashed_password, email=data['email'], full_name=data['full_name'], role='clerk', store_id=data['store_id'])

        new_user.save()

        return marshal(new_user, signup_model), 201


if __name__ == '__main__':
    app.run(debug=True)