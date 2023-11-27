
from flask import Flask
from flask_cors import CORS
from flask_restx import Api


from .config.config import config_dict
from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models.association import store_product_association
from .models.users import Users
from .models.stores import Store
from .models.products import Products
from .models.supplyrequests import SupplyRequests
from .models.suppliers import Suppliers
from .models.sales import Sales
from .models.receipts import Receipts
from flask_mail import Mail, Message
from .email.views import email_namespace
from .login.loginapi import login_namespace
from .stores.views import store_namespace
# from .models.stores import Store

def create_app():
    app=Flask(__name__)
    app.config.from_object(config_dict['dev'])
    mail=Mail(app)
    # initialize database
    db.init_app(app)
    CORS(app)
    

    
    
    
    jwt = JWTManager(app)

    migrate=Migrate(app, db)
    
    api=Api(app)
    

    # api blueprints - used for documentation
    api.add_namespace(email_namespace)
    api.add_namespace(login_namespace)
    api.add_namespace(store_namespace)
   
    
    with app.app_context():
        db.create_all()
        
        
        




    # @app.shell_context_processor
    # def make_shell_context():
    #     return {
    #         'db':db,
    #         'User':User,
    #         'Messages':Messages,
    #         'ChatRoom':ChatRoom,
    #         'hub':Hub
    #     }
    return app