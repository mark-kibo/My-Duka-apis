

from flask import Flask
from flask_cors import CORS
from api import create_app

app = create_app()
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5000", "http://localhost:3000"]}})



# app.run()