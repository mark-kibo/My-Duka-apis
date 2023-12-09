# Import necessary modules
# from flask_sqlalchemy import SQLAlchemy
import werkzeug.security
from ..utils import db
from flask_restx import Api, fields, marshal, Resource, Namespace,reqparse
from ..models.users import User 

from http import HTTPStatus


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
    # @get_users_namespace.marshal_with(user_model, as_list=True)
    @get_users_namespace.doc(
    description="get all merchants"
)
    def get(self):
        merchants = User.query.filter_by(role='merchant').all()
        if not merchants:
            return {"message": "No clerks registered"}, HTTPStatus.NOT_FOUND
        return marshal(merchants, user_model), HTTPStatus.OK

    @get_users_namespace.expect(user_parser)
    @get_users_namespace.doc(
    description="create a merchant"
)
    def post(self):
        try:
            args = user_parser.parse_args()
            new_merchant = User(
                username=args['username'],
                password=args['password'],
                email=args['email'],
                full_name=args['full_name'],
                role='merchant',
                store_id=args['store_id']
            )
            new_merchant.save()    
            return marshal(new_merchant, user_model), 201
        except:
            return marshal(new_merchant, user_model), HTTPStatus.OK
    

    @get_users_namespace.route('/merchants/<int:merchant_id>')
    
    class MerchantResource(Resource):
        @get_users_namespace.marshal_with(user_model)
        @get_users_namespace.doc(
    description="get merchant by id"
)
        def get(self, merchant_id):
            merchant = User.query.get(merchant_id)
            if not merchant:
                 return {"message": "No merchant  with that id"}, HTTPStatus.NOT_FOUND
            return marshal(merchant, user_model)

        @get_users_namespace.expect(user_parser)
        
        
        
        @get_users_namespace.doc(
            description="update merchant resource"
        )
        def put(self, merchant_id):
            try:
                merchant = User.query.get(merchant_id)
                
                if not merchant:
                    return {"message": "No merchant exists with that Id"}, HTTPStatus.NOT_FOUND
                args = user_parser.parse_args()
                merchant.username = args['username']
                merchant.password = args['password']
                merchant.email = args['email']
                merchant.full_name = args['full_name']
                merchant.store_id = args['store_id']
                
                merchant.save()
                return marshal(merchant, user_model), HTTPStatus.OK
            except:
                return {"message": "cant update resource"}, HTTPStatus.BAD_REQUEST
        
        @get_users_namespace.doc(
            description="delete merchant by id"
        )
        def delete(self, merchant_id):
            merchant = User.query.get(merchant_id)
            if not merchant:
                    return {"message": "No merchant exists with that Id"}, HTTPStatus.NOT_FOUND
            merchant.delete()
            return {'message': 'Merchant deleted successfully'}, 200

@get_users_namespace.route('/admins')
class GetAdminsResource(Resource):
    def get(self):
        admins = User.query.filter_by(role='admin').all() 
        if not admins:
                    return {"message": "no admins exists"}, HTTPStatus.NOT_FOUND
        return marshal(admins, user_model), 200

    @get_users_namespace.expect(user_parser)
    def post(self):
        
        try:
            args = user_parser.parse_args()
            new_admin = User(
                username=args['username'],
                password=args['password'],
                email=args['email'],
                full_name=args['full_name'],
                role='admin',
                store_id=args['store_id']
            )
            new_admin.save()
            return marshal(new_admin,user_model)  , 201
        
        except:
            return {"message": "cant create admin"}, 404

    @get_users_namespace.route('/admins/<int:admin_id>')
    class AdminResource(Resource):
        
        def get(self, admin_id):
            admin = User.query.get(admin_id)
            if not admin:
                return {"message":"no admin with that id"}, 404
            return marshal(admin, user_model)

        @get_users_namespace.expect(user_parser)
        def put(self, admin_id):
            try:
                admin = User.query.get(admin_id)
                if not admin:
                    return {"message":"no admin with that id"}, 404
                args = user_parser.parse_args()
                admin.username = args['username']
                admin.password = args['password']
                admin.email = args['email']
                admin.full_name = args['full_name']
                admin.store_id = args['store_id']
                
                admin.save()
                return marshal(admin, user_model)
            except:
                return {"message": "cant update admin"}, 400

        def delete(self, admin_id):
            admin = User.query.get(admin_id)
            if not admin:
                return {"message": "no admin with that id"}, 404

            admin.delete()
            return {'message': 'Admin deleted successfully'}, 200

@get_users_namespace.route('/clerks')
class GetClerksResource(Resource):
    def get(self):
        clerks = User.query.filter_by(role='clerk').all()
        if not clerks:
            return {"message":"no clerks found "}, 404
        return marshal(clerks, user_model)
    
    @get_users_namespace.expect(user_parser)
    def post(self):
        try:
            args = user_parser.parse_args()
            new_clerk = User(
                username=args['username'],
                password=args['password'],
                email=args['email'],
                full_name=args['full_name'],
                role='clerk',
                store_id=args['store_id']
            )
            new_clerk.save()
            return marshal(new_clerk, user_model)
        except:
            
            return {"message": "cant create admin"}, 400
    @get_users_namespace.route('/clerks/<int:clerk_id>')
    class ClerkResource(Resource):
        @get_users_namespace.marshal_with(user_model)
        def get(self, clerk_id):
            clerk = User.query.get(clerk_id)
            if not clerk:
                return {"message":"no clerk with that id"}, 404
            return marshal(clerk, user_model)

        @get_users_namespace.expect(user_parser)
        def put(self, clerk_id):
            try:
                clerk = User.query.get(clerk_id)
                args = user_parser.parse_args()
                clerk.username = args['username']
                clerk.password = args['password']
                clerk.email = args['email']
                clerk.full_name = args['full_name']
                clerk.store_id = args['store_id']
                
                clerk.save()
                return marshal(clerk, user_model)
            except:
                return {"message": "cant update clerk"}, 400

        def delete(self, clerk_id):
            clerk = User.query.get(clerk_id)
            if clerk:
                clerk.save()
                return {'message': 'Clerk deleted successfully'}, 200
            else:
                return {'message': 'Clerk not found'}, 404




    


