from flask_sqlalchemy import SQLAlchemy



db=SQLAlchemy()

store_product_association = db.Table(
    'store_product_association',
    db.Column('store_id', db.Integer(), db.ForeignKey('store.store_id')),
    db.Column('product_id', db.Integer(), db.ForeignKey('products.product_id'))
)