from itsdangerous import URLSafeTimedSerializer
from flask_restx import Namespace, Resource, fields, marshal_with
from flask import request, url_for, redirect
from http import HTTPStatus
from flask_mail import Message
from ..utils import mail

# initialize tokenize email - takes a secret key
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

@email_namespace.route("/email")
class TokenizeEmail(Resource):
    @email_namespace.expect(getmail_model)
    def post(self):
        data = request.get_json()
        print(data.get("email"))
        
        # create the token
        token = s.dumps(data.get("email"), salt="email-confirm")
        
        # create email message
        msg=Message("email", sender="kibochamark@gmail.com" ,  recipients=[data.get("email")])

        print(msg)
        link = '<a href="http://127.0.0.1:5000/custom-url">Click here</a>'
        
        msg.body = "Your link is {}".format(link)
        
        mail.send(msg)
        
        return token, HTTPStatus.OK
    
    
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