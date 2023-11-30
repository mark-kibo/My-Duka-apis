
from ..utils import db
from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace, fields, marshal_with
from api.models.receipts import Receipts




api = Api()


receipts_namespace = Namespace('receipts', description='receipts endpoints')


receipt_parser = reqparse.RequestParser()
receipt_parser.add_argument('date_time', type=str, required=True, help='Date and time of the receipt')
receipt_parser.add_argument('product_id', type=int, required=True, help='ID of the product')
receipt_parser.add_argument('quantity_received', type=int, required=True, help='Quantity received')
receipt_parser.add_argument('payment_status', type=str, required=True, help='Payment status')


receipt_model = api.model('Receipt', {
    'receipt_id': fields.Integer,
    'date_time': fields.String,
    'product_id': fields.Integer,
    'quantity_received': fields.Integer,
    'payment_status': fields.String,
})







@receipts_namespace.route('/')
class ReceiptsResource(Resource):
    @marshal_with(receipt_model, envelope='receipts')
    def get(self):
        receipts = Receipts.query.all()
        return receipts

    @marshal_with(receipt_model)
    def post(self):
        args = receipt_parser.parse_args()

        new_receipt = Receipts(
            date_time=args['date_time'],
            product_id=args['product_id'],
            quantity_received=args['quantity_received'],
            payment_status=args['payment_status']
        )

        db.session.add(new_receipt)
        db.session.commit()

        return new_receipt


@receipts_namespace.route('/<int:receipt_id>')
class ReceiptResource(Resource):
    @marshal_with(receipt_model)
    def get(self, receipt_id):
        receipt = Receipts.query.filter_by(receipt_id=receipt_id).first()
        return receipt

    @marshal_with(receipt_model)
    def patch(self, receipt_id):
        args = receipt_parser.parse_args()
        receipt = Receipts.query.filter_by(receipt_id=receipt_id).first()

        receipt.date_time = args['date_time']
        receipt.product_id = args['product_id']
        receipt.quantity_received = args['quantity_received']
        receipt.payment_status = args['payment_status']

        db.session.commit()

        return receipt

    def delete(self, receipt_id):
        receipt = Receipts.query.filter_by(receipt_id=receipt_id).first()
        db.session.delete(receipt)
        db.session.commit()
        return {'message': 'Receipt deleted successfully'}





