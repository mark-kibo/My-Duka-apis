from flask_restx import Namespace, Resource, fields, reqparse, marshal
from flask import request
from http import HTTPStatus
from ..models.supplyrequests import SupplyRequests

supply_requests_namespace = Namespace("supply_requests", "Supply Requests Endpoints")

# Define the model for serialization
supply_request_model = supply_requests_namespace.model('SupplyRequest', {
    'request_id': fields.Integer(description='The unique identifier of a supply request'),
    'clerk_id': fields.Integer(description='Clerk ID'),
    'product_id': fields.Integer(description='Product ID'),
    'quantity_requested': fields.Integer(description='Quantity Requested'),
    'reason_for_request': fields.String(description='Reason for Request'),
    'received_items': fields.Integer(description='Received Items'),
    'received': fields.Boolean(description='Received Status'),
    'approved': fields.Boolean(description='Approval Status'),
})

# Parser for request arguments
supply_request_parser = reqparse.RequestParser()
supply_request_parser.add_argument('clerk_id', type=int, required=True, help='Clerk ID is required')
supply_request_parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
supply_request_parser.add_argument('quantity_requested', type=int, required=True, help='Quantity Requested is required')
supply_request_parser.add_argument('reason_for_request', type=str, required=True, help='Reason for Request is required')

@supply_requests_namespace.route("/")
class SupplyRequestList(Resource):
    @supply_requests_namespace.marshal_list_with(supply_request_model)
    def get(self):
        """Get all supply requests"""
        try:
            supply_requests = SupplyRequests.query.all()
            return marshal(supply_requests, supply_request_model), HTTPStatus.OK
        except Exception as e:
            return {"error": "Internal Server Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @supply_requests_namespace.expect(supply_request_model)
    @supply_requests_namespace.marshal_with(supply_request_model, code=HTTPStatus.CREATED)
    def post(self):
        """Create a new supply request"""
        try:
            data = supply_request_parser.parse_args()
            new_supply_request = SupplyRequests(**data)
            new_supply_request.save()
            return marshal(new_supply_request, supply_request_model), HTTPStatus.CREATED
        except Exception as e:
            return {"error": "Bad Request"}, HTTPStatus.BAD_REQUEST

@supply_requests_namespace.route("/<int:request_id>")
class SupplyRequest(Resource):
    @supply_requests_namespace.marshal_with(supply_request_model)
    def get(self, request_id):
        """Get details of a specific supply request by its ID"""
        try:
            supply_request = SupplyRequests.query.get_or_404(request_id)
            return marshal(supply_request, supply_request_model), HTTPStatus.OK
        except Exception as e:
            return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    @supply_requests_namespace.expect(supply_request_model)
    @supply_requests_namespace.marshal_with(supply_request_model)
    def patch(self, request_id):
        """Update an existing supply request"""
        try:
            supply_request = SupplyRequests.query.get_or_404(request_id)
            data = supply_request_parser.parse_args()
            for attr in data:
                setattr(supply_request, attr, data.get(attr))
            supply_request.save()
            return marshal(supply_request, supply_request_model), HTTPStatus.OK
        except Exception as e:
            return {"error": "Bad Request"}, HTTPStatus.BAD_REQUEST

    def delete(self, request_id):
        """Delete a supply request"""
        try:
            supply_request = SupplyRequests.query.get_or_404(request_id)
            supply_request.delete()
            return {"message": f"Successfully deleted supply request with id '{request_id}'"}, HTTPStatus.NO_CONTENT
        except Exception as e:
            return {"error": "Bad Request"}, HTTPStatus.BAD_REQUEST
