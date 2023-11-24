from ..utils import db

class Users(db.Model):
    __tablename__= "users"

    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'))

  
    # Define the foreign key relationship for the stores
    stores = db.relationship('Store', backref='user', lazy=True, foreign_keys='Store.user_id')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
