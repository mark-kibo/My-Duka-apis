from ..utils import db

class Receipts(db.Model):
    __tablename__ = 'receipts'

    receipt_id = db.Column(db.Integer(), primary_key=True)
    date_time = db.Column(db.DateTime())
    product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'))
    quantity_received = db.Column(db.Integer())
    payment_status = db.Column(db.String(50))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()