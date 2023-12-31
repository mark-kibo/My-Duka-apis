from ..utils import db
from .stores import Store
from .supplyrequests import SupplyRequests

class User(db.Model):
    __tablename__= "users"

    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=True)
    
    # Define the foreign key relationship for the stores
    stores = db.relationship('Store', backref='user', foreign_keys=[store_id])
    supply_requests = db.relationship('SupplyRequests', backref='user', cascade='all, delete-orphan')

    def save(self):
        db.session.add(self)
        db.session.commit()
        
        # Create a store for the user if not already associated with one and the role is 'merchant'
        # if self.role == 'merchant' and not self.stores:
        #     store = Store(user=[self])
        #     db.session.add(store)
        #     db.session.commit()

    def delete(self):
        # Check the role before deletion
        if self.role == 'merchant':
            # Delete the associated store and its users
            if self.stores:
                store = self.stores  # Assuming a user can be associated with only one store
                store.delete()
        else:
            # For users with roles other than 'merchant', set store_id to null
            if self.stores:
                store = self.stores # Assuming a user can be associated with only one store
                store.user_id = None

        db.session.delete(self)
        db.session.commit()
