from ..utils import db

class Suppliers(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column(db.Integer(), primary_key=True)
    supply_name = db.Column(db.String(255))
    supplier_contact = db.Column(db.String(50))
    supplier_email = db.Column(db.String(255))
    supplier_address = db.Column(db.String(255))

    products = db.relationship('Products', back_populates='supplier', lazy=True)