from ..utils import db
from .association import store_product_association

class Products(db.Model):
    __tablename__ = 'products'


    product_id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    category = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    quantity = db.Column(db.Integer())
    buying_price = db.Column(db.Integer())
    selling_price = db.Column(db.Integer())
    payment_status = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'),  nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)

    receipts = db.relationship('Receipts', backref='product', lazy=True)
    supply_requests = db.relationship('SupplyRequests', backref='product', lazy=True)
    stores = db.relationship('Store', back_populates='products_association', lazy=True)

    # Relationship with the 'Store' table through the association table
    stores = db.relationship('Store', secondary=store_product_association, back_populates='products')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()