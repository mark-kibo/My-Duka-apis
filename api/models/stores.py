from ..utils import db
from .association import store_product_association

class Store(db.Model):
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer(), primary_key=True)
    store_name=db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    location = db.Column(db.String(255))
    
  # Relationship with the 'Products' table through the association table
    products = db.relationship('Products', secondary=store_product_association, back_populates='stores')
    
    supplier_id = db.Column(db.Integer(), db.ForeignKey('suppliers.supplier_id'), nullable=True)


