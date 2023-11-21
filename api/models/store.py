from ..utils import db, store_product_association
class Store(db.Model):
    store_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    location = db.Column(db.String(255))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'))
    supplier_id = db.Column(db.Integer(), db.ForeignKey('suppliers.supplier_id'))

Store.receipts = db.relationship('Receipts', backref='store', lazy=True)
Store.suppliers = db.relationship('Suppliers', backref='store', lazy=True)
Store.sales = db.relationship('Sales', backref='store', lazy=True)


Store.products_association = db.relationship('Products', secondary=store_product_association, back_populates='stores_association')
