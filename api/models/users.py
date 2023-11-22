from ..utils import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'))

    def __init__(self, username, email, full_name, password, role, store_id=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.store_id = store_id

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Relationships
Users.products = db.relationship('Products', backref='user', lazy=True)
Users.stores = db.relationship('Store', backref='user', lazy=True)
