from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash


from ..models.users import User

login_namespace = Namespace('login', description='login endpoints')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
login_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

login_model=login_namespace.model('Login', {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})
@login_namespace.route('/')
class LoginResource(Resource):
    
    @login_namespace.expect(login_model)
    def post(self):
        data = login_parser.parse_args()

        username = data['username']
        password = data['password']

        # Assuming you have a User model with 'username', 'user_id', and 'role' fields
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # You can customize the token to include additional information
            access_token = create_access_token(identity=user.user_id, additional_claims={'username': user.username, 'id': user.user_id, 'role': user.role})
            return {'message': 'login successful', 'access_token': access_token}

        # Handle possible errors
        return {'message': 'Invalid credentials'}, 401
