from ..utils import db

class Suppliers(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column(db.Integer(), primary_key=True)
    supply_name = db.Column(db.String(255))
    supplier_contact = db.Column(db.String(50))
    supplier_email = db.Column(db.String(255))
    supplier_address = db.Column(db.String(255))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'), nullable=True)
    store_id = db.Column(db.Integer(), db.ForeignKey('stores.store_id'))
def save(self):
        db.session.add(self)
        db.session.commit()

def delete(self):
        db.session.delete(self)
        db.session.commit()