

from flask import Flask
from flask_cors import CORS
from api import create_app

app = create_app()
CORS(app, resources={r"/api/*": {"origins": "*"}})



# app.run()