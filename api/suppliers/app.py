from flask_restx import Namespace, Resource, fields, reqparse, marshal
from flask import request
from http import HTTPStatus
from ..models.suppliers import Suppliers
from ..utils import db

suppliers_namespace = Namespace("suppliers", "Suppliers endpoints")

supplier_model = suppliers_namespace.model('supplier', {
    'supplier_id': fields.Integer(description='The unique identifier of a supplier'),
    'supply_name': fields.String(description='The name of the supplier'),
    'supplier_contact': fields.String(description='The contact information of the supplier'),
    'supplier_email': fields.String(description='The email address of the supplier'),
    'supplier_address': fields.String(description='The address of the supplier'),
    'product_id': fields.Integer(description='The product supplied by the supplier'),
    'store_id': fields.Integer(description='The store associated with the supplier'),
})

supplier_parser = reqparse.RequestParser()
supplier_parser.add_argument('supply_name', type=str, required=True, help='Name of the supplier')
supplier_parser.add_argument('supplier_contact', type=str, required=True, help='Contact information of the supplier')
supplier_parser.add_argument('supplier_email', type=str, required=True, help='Email address of the supplier')
supplier_parser.add_argument('supplier_address', type=str, required=True, help='Address of the supplier')
supplier_parser.add_argument('product_id', type=int, required=True, help='Product supplied by the supplier')
supplier_parser.add_argument('store_id', type=int, required=True, help='Store associated with the supplier')

@suppliers_namespace.route("/")
class SuppliersList(Resource):
    def get(self):
        try:
            suppliers = Suppliers.query.all()
            print(suppliers)

            if suppliers:
                return {'suppliers': [marshal(supplier, supplier_model) for supplier in suppliers]}, HTTPStatus.OK
            else:
                return {"message": "No suppliers found"}, HTTPStatus.OK
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST

    @suppliers_namespace.expect(supplier_parser)
    def post(self):
        try:
            data = supplier_parser.parse_args()

            new_supplier = Suppliers(
                supply_name=data['supply_name'],
                supplier_contact=data['supplier_contact'],
                supplier_email=data['supplier_email'],
                supplier_address=data['supplier_address'],
                product_id=data['product_id'],
                store_id=data['store_id']
            )

            new_supplier.save()

            return marshal(new_supplier, supplier_model), HTTPStatus.CREATED
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST

@suppliers_namespace.route("/<int:id>")
class MutateSupplier(Resource):
    def get(self, id):
        try:
            supplier = Suppliers.query.get(id)

            if not supplier:
                return {"message": f"Supplier with id '{id}' doesn't exist."}, HTTPStatus.NOT_FOUND

            return marshal(supplier, supplier_model), HTTPStatus.OK
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST

    @suppliers_namespace.expect(supplier_parser)
    def patch(self, id):
        try:
            supplier = Suppliers.query.get(id)

            if not supplier:
                return {"message": f"Supplier with id '{id}' doesn't exist."}, HTTPStatus.NOT_FOUND

            data = supplier_parser.parse_args()

            for attr in data:
                setattr(supplier, attr, data[attr])

            supplier.save()

            return marshal(supplier, supplier_model, skip_none=True), HTTPStatus.OK
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST

    def delete(self, id):
        try:
            supplier = Suppliers.query.get(id)

            if not supplier:
                return {"message": f"Supplier with id '{id}' doesn't exist."}, HTTPStatus.NOT_FOUND

            supplier.delete()

            return {"message": f"Successfully deleted supplier with id '{id}'"}, HTTPStatus.NO_CONTENT
        except Exception as e:
            print(f"Error: {e}")
            return {"error": "Bad request"}, HTTPStatus.BAD_REQUEST
