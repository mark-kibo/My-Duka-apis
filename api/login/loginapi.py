from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash


from ..models.users import Users

login_namespace = Namespace('login', description='Login operations')

login_model = login_namespace.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@login_namespace.route('/')
class LoginResource(Resource):
    @login_namespace.expect(login_model)
    def post(self):
        
        data = login_namespace.payload

        username = data['username']
        password = data['password']

        # user = Users.query.filter_by(username=username).first()
        user = Users(username='mercy', password='password')

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid username or password'}, 401