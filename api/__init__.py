
from flask import Flask
from flask_cors import CORS
from flask_restx import Api


from .config.config import config_dict
from .utils import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.signup.signupapi import signup_namespace
from api.login.loginapi import login_namespace


def create_app():
    app = Flask(__name__)

    app.config.from_object(config_dict['dev'])
    # initialize database
    
    # db.init_app(app)
    CORS(app)

    
    
    # initialize database
    db.init_app(app)
    jwt=JWTManager(app)

    migrate=Migrate(app, db)
    
    api=Api(app)

    api.add_namespace(signup_namespace)
    api.add_namespace(login_namespace)
    




    # @app.shell_context_processor
    # def make_shell_context():
    #     return {
    #         'db': db,
    #         'User': User,
    #         'Messages': Messages,
    #         'ChatRoom': ChatRoom,
    #         'hub': Hub
    #     }
    return app



