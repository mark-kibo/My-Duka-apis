# Import necessary modules
# from flask_sqlalchemy import SQLAlchemy
import werkzeug.security
from ..utils import db
from flask_restx import Api, fields, Resource, Namespace,reqparse
from ..models.users import User 
from flask_bcrypt import check_password_hash


api = Api()


get_users_namespace = Namespace('users', description='users endpoints')
user_model = get_users_namespace.model('User', {
    'username': fields.String(description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(description='Email'),
    'full_name': fields.String(description='Full Name'),
    'role': fields.String(description='Role'),
    'store_id': fields.Integer(description='Store ID')
})




user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username of the clerk')
user_parser.add_argument('password', type=str, required=True, help='Password of the clerk')
user_parser.add_argument('email', type=str, required=True, help='Email of the clerk')
user_parser.add_argument('full_name', type=str, required=True, help='Full name of the clerk')
user_parser.add_argument('store_id', type=int, required=True, help='Store ID of the clerk')



@get_users_namespace.route('/all-users')
class GetAllUsersResource(Resource):
    @get_users_namespace.marshal_with(user_model, as_list=True)
    def get(self):
        all_users = User.query.all()
        return all_users


@get_users_namespace.route('/merchants')
class GetMerchantsResource(Resource):
    @get_users_namespace.marshal_with(user_model, as_list=True)
    def get(self):
        merchants = User.query.filter_by(role='merchant').all()
        return merchants

    @get_users_namespace.expect(user_parser)
    @get_users_namespace.marshal_with(user_model)
    def post(self):
        args = user_parser.parse_args()
        new_merchant = User(
            username=args['username'],
            password=args['password'],
            email=args['email'],
            full_name=args['full_name'],
            role='merchant',
            store_id=args['store_id']
        )
        db.session.add(new_merchant)
        db.session.commit()
        return new_merchant, 201

@get_users_namespace.route('/merchants/<int:merchant_id>')
class MerchantResource(Resource):
        @get_users_namespace.marshal_with(user_model)
        def get(self, merchant_id):
            merchant = User.query.get(merchant_id)
            return merchant

        @get_users_namespace.expect(user_parser)
        @get_users_namespace.marshal_with(user_model)
        def put(self, merchant_id):
            merchant = User.query.get(merchant_id)
            args = user_parser.parse_args()
            merchant.username = args['username']
            merchant.password = args['password']
            merchant.email = args['email']
            merchant.full_name = args['full_name']
            merchant.store_id = args['store_id']
            db.session.commit()
            return merchant

        def delete(self, merchant_id):
            merchant = User.query.get(merchant_id)
            db.session.delete(merchant)
            db.session.commit()
            return {'message': 'Merchant deleted successfully'}, 200

@get_users_namespace.route('/admins')
class GetAdminsResource(Resource):
    @get_users_namespace.marshal_with(user_model, as_list=True)
    def get(self):
        admins = User.query.filter_by(role='admin').all()
        return admins

    @get_users_namespace.expect(user_parser)
    @get_users_namespace.marshal_with(user_model)
    def post(self):
        args = user_parser.parse_args()
        new_admin = User(
            username=args['username'],
            password=args['password'],
            email=args['email'],
            full_name=args['full_name'],
            role='admin',
            store_id=args['store_id']
        )
        db.session.add(new_admin)
        db.session.commit()
        return new_admin, 201

@get_users_namespace.route('/admins/<int:admin_id>')
class AdminResource(Resource):
        @get_users_namespace.marshal_with(user_model)
        def get(self, admin_id):
            admin = User.query.get(admin_id)
            return admin

        @get_users_namespace.expect(user_parser)
        @get_users_namespace.marshal_with(user_model)
        def put(self, admin_id):
            admin = User.query.get(admin_id)
            args = user_parser.parse_args()
            admin.username = args['username']
            admin.password = args['password']
            admin.email = args['email']
            admin.full_name = args['full_name']
            admin.store_id = args['store_id']
            db.session.commit()
            return admin

        def delete(self, admin_id):
            admin = User.query.get(admin_id)
            db.session.delete(admin)
            db.session.commit()
            return {'message': 'Admin deleted successfully'}, 200

@get_users_namespace.route('/clerks')
class GetClerksResource(Resource):
    @get_users_namespace.marshal_with(user_model, as_list=True)
    def get(self):
        clerks = User.query.filter_by(role='clerk').all()
        return clerks

    @get_users_namespace.expect(user_parser)
    @get_users_namespace.marshal_with(user_model)
    def post(self):
        args = user_parser.parse_args()
        new_clerk = User(
            username=args['username'],
            password=args['password'],
            email=args['email'],
            full_name=args['full_name'],
            role='clerk',
            store_id=args['store_id']
        )
        db.session.add(new_clerk)
        db.session.commit()
        return new_clerk, 201

@get_users_namespace.route('/clerks/<int:clerk_id>')
class ClerkResource(Resource):
        @get_users_namespace.marshal_with(user_model)
        def get(self, clerk_id):
            clerk = User.query.get(clerk_id)
            return clerk

        @get_users_namespace.expect(user_parser)
        @get_users_namespace.marshal_with(user_model)
        def put(self, clerk_id):
            clerk = User.query.get(clerk_id)
            args = user_parser.parse_args()
            clerk.username = args['username']
            clerk.password = args['password']
            clerk.email = args['email']
            clerk.full_name = args['full_name']
            clerk.store_id = args['store_id']
            db.session.commit()
            return clerk

        def delete(self, clerk_id):
            clerk = User.query.get(clerk_id)
            if clerk:
                db.session.delete(clerk)
                db.session.commit()
                return {'message': 'Clerk deleted successfully'}, 200
            else:
                return {'message': 'Clerk not found'}, 404




    


