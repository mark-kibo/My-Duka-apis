from ..utils import db
class Suppliers(db.Model):
    supplier_id = db.Column(db.Integer(), primary_key=True)
    supply_name = db.Column(db.String(100))
    supplier_contact = db.Column(db.String(50))
    supplier_email = db.Column(db.String(100))
    supplier_address = db.Column(db.String(255))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'))
    store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'))


Suppliers.products = db.relationship('Products', backref='supplier', lazy=True)
Suppliers.stores = db.relationship('Store', backref='supplier', lazy=True)