from ..utils import db


class Sales(db.Model):
    __tablename__ = 'sales'

    sale_id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    product_quantity = db.Column(db.Integer())
    store_id = db.Column(db.Integer(), db.ForeignKey('stores.store_id'))
    amount = db.Column(db.Integer())
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
