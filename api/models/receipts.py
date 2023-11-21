from ..utils import db
class Receipts(db.Model):
    receipt_id = db.Column(db.Integer(), primary_key=True)
    date_time_of_receipt = db.Column(db.DateTime())
    product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'))
    quantity_received = db.Column(db.Integer())
    payment_status = db.Column(db.String(20))
