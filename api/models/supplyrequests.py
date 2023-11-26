from ..utils import db

class SupplyRequests(db.Model):
    __tablename__ = 'supply_requests'

    request_id = db.Column(db.Integer(), primary_key=True)
    clerk_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'))
    quantity_requested = db.Column(db.Integer())
    reason_for_request = db.Column(db.String(255))
    received_items = db.Column(db.Integer())
    received = db.Column(db.Boolean())
    approved = db.Column(db.Boolean())