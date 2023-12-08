from itsdangerous import URLSafeTimedSerializer
from flask_restx import Namespace, Resource, fields, marshal_with
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, url_for, redirect
from http import HTTPStatus
from flask_mail import Message
from ..utils import mail
from ..models.users import User


s= URLSafeTimedSerializer("myduka")

email_namespace=Namespace("email", "get tokenized email")
email_model=email_namespace.model(
    
    "Email",{
        "link":fields.String
    }
)
getmail_model=email_namespace.model(
    
    "Email",{
        "email":fields.String()
    }
)

def get_current_user():
    jwt_required()  
    user_id = get_jwt_identity()

    return User.query.get(user_id)


@email_namespace.route("/email")
class TokenizeEmail(Resource):
    @jwt_required()
    @email_namespace.expect(getmail_model)
    def post(self):
        data = request.get_json()
        user_email = data.get("email")

        
        current_user = get_current_user()
        # msg = Message("email", sender=current_user.email, recipients=[user_email])


        if current_user and current_user.role == 'merchant':
            
            token = s.dumps(user_email, salt="email-confirm")

           
            msg = Message("email", sender="chepmercy21@gmail.com", recipients=[user_email])

            link = f'https://my-duka-front-kup405jo7-mark-kibo.vercel.app/signup/{token}'
            msg.body = "copy this link to your browser is {}".format(link)

            mail.send(msg)

            return token, HTTPStatus.OK
        else:
            return {"error": "Unauthorized"}, HTTPStatus.UNAUTHORIZED    
    
@email_namespace.route("/email/<token>")
class ConfirmTokenizeEmail(Resource):
    def get(self, token):
        try:
                
            # confirm the tokenized email
            email = s.loads(token, salt="email-confirm", max_age=60)
            print(email)
            
            if email:
                return email,  HTTPStatus.OK
            
            else:
                return {
                    "error":"Token expired"
                },  HTTPStatus.FORBIDDEN
        except:
            return {
                    "error":"Token expired"
                }, HTTPStatus.FORBIDDEN