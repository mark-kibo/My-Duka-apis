from ..utils import db

class SupplyRequests(db.Model):
    __tablename__ = 'supply_requests'

    request_id = db.Column(db.Integer(), primary_key=True)
    users_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    quantity_requested = db.Column(db.Integer())
    reason_for_request = db.Column(db.String(255))
    received_items = db.Column(db.Integer())
    received = db.Column(db.Boolean())
    approved = db.Column(db.Boolean())


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()