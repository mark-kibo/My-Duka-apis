from ..utils import db
class Users(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'))



# Relationships
Users.products = db.relationship('Products', backref='user', lazy=True)
Users.stores = db.relationship('Store', backref='user', lazy=True)