from ..utils import db, store_product_association
class Products(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    category = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    quantity = db.Column(db.Integer())
    buying_price = db.Column(db.Float())
    selling_price = db.Column(db.Float())
    payment_status = db.Column(db.String(20))
    image_url = db.Column(db.String(255))
    store_id = db.Column(db.Integer(), db.ForeignKey('store.store_id'))
    supplier_id = db.Column(db.Integer(), db.ForeignKey('suppliers.supplier_id'))


Products.receipts = db.relationship('Receipts', backref='product', lazy=True)
Products.supply_requests = db.relationship('SupplyRequests', backref='product', lazy=True)
Products.stores = db.relationship('Store', backref='product', lazy=True)

Products.stores_association = db.relationship('Store', secondary=store_product_association, back_populates='products_association')