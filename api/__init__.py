
from flask import Flask
from flask_cors import CORS
from flask_restx import Api


from .config.config import config_dict
from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models.association import store_product_association
from .models.users import User
from .models.stores import Store
from .models.products import Products
from .models.supplyrequests import SupplyRequests
from .models.suppliers import Suppliers
from .models.sales import Sales
from .models.receipts import Receipts
from flask_mail import Mail, Message
from .email.views import email_namespace
from .signup.signupapi import signup_namespace

from .users.getusersapi import get_users_namespace
from .Receipt.receiptsapi import receipts_namespace
from .suppliers.app import suppliers_namespace
from .login.loginapi import login_namespace
from .stores.views import store_namespace
from .products.views import products_namespace
from .users.getusersapi import get_users_namespace
from .supplyrequests.app import supply_requests_namespace
from .signup.signupapi import signup_namespace
from .sales.views import sales_namespace

# from .models.stores import Store







def create_app():
    app=Flask(__name__)
    CORS(app)
    app.config.from_object(config_dict['dev'])
    mail=Mail(app)



    # bcrypt = Bcrypt(app)
    # initialize database
    
    db.init_app(app)
    CORS(app)
    

    
    

    
    jwt = JWTManager(app)
    # bycrypt = Bcrypt(app)


    migrate=Migrate(app, db)
    
    authorizations={
        "Bearer AUth":{
            'type': 'apikey',
            'in': 'header',
            "name": 'Authorization',
            'description': 'Add a JWT with ** Bearer &lt;JWT&gt; to authorize'
        }
    }
    
    api=Api(app,
            title="My duka apis",
            description="Endpoints to access My duka stores, users, sales and suppliers")
        
    api.add_namespace(email_namespace)
    api.add_namespace(signup_namespace) 
    # api blueprints - used for documentation
  
    api.add_namespace(signup_namespace)
    api.add_namespace(login_namespace)
    api.add_namespace(email_namespace)
    api.add_namespace(store_namespace)
    
    api.add_namespace(products_namespace)
    api.add_namespace(store_namespace)
    api.add_namespace(get_users_namespace)
    api.add_namespace(store_namespace)
    api.add_namespace(products_namespace)
    api.add_namespace(sales_namespace) 
    api.add_namespace(suppliers_namespace)
    api.add_namespace(supply_requests_namespace)
    api.add_namespace(receipts_namespace)
    
   
   
    
    
   
    
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
