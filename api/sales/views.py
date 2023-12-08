from flask import request
from flask_restx import Namespace, marshal, fields, Resource
from http import HTTPStatus
from ..models.sales import Sales
from ..models.products import Products


sales_namespace= Namespace("sales", "sales endpoints")
# Define the Sale model for API input
sale_model = sales_namespace.model('Sale', {
    'product_id': fields.Integer(required=True, description='Product ID'),
    'product_quantity': fields.Integer(required=True, description='Product Quantity'),
    'store_id': fields.Integer(required=True, description='Store ID'),
    'amount': fields.Integer(required=True, description='Amount'),
})


# Resource for creating a new sale
@sales_namespace.route('/create')
class CreateSaleResource(Resource):
    @sales_namespace.expect(sale_model)
    def post(self):
        data = request.get_json()
        product_id = data['product_id']
        product_quantity = data['product_quantity']
        store_id = data['store_id']
        amount = data['amount']

        # Check if the product exists and has enough quantity
        # You need to implement this logic based on your application's structure

        # Assuming you have a Product model
        product = Products.query.get(product_id=product_id)

        if not product or product.quantity < product_quantity:
            return {'message': 'Product not found or not enough quantity'}, HTTPStatus.NOT_FOUND

        # Create a new sale
        sale = Sales(
            product_id=product_id,
            product_quantity=product_quantity,
            store_id=store_id,
            amount=amount
        )

        # Reduce the product quantity
        product.quantity -= product_quantity

        # Save to the database
        sale.save()

        return marshal(sale, sale_model), HTTPStatus.CREATED
    
    

@sales_namespace.route('/get_all')
class GetAllSalesResource(Resource):
    def get(self):
        sales = Sales.query.all()
        
        if not sales:
            return {"message":"no sales available"}, HTTPStatus.OK
        
        return marshal(sales, sale_model), HTTPStatus.OK
    
    
    
# Resource for getting a sale by ID
@sales_namespace.route('/get/<int:sale_id>')
class GetSaleByIdResource(Resource):
    def get(self, sale_id):
        sale = Sales.query.get(sale_id=sale_id)
        if sale:
            return marshal(sale, sale_model), HTTPStatus.OK
        return {'message': 'Sale not found'}, HTTPStatus.NOT_FOUND
    
    
# Resource for updating a sale by ID (patch)
@sales_namespace.route('/patch/<int:sale_id>')
class PatchSaleResource(Resource):
    @sales_namespace.expect(sale_model)
    def patch(self, sale_id):
        sale = Sales.query.get(sale_id=sale_id)
        if not sale:
            return {'message': 'Sale not found'}, HTTPStatus.NOT_FOUND

        data = request.get_json()
        product_quantity = data['product_quantity']
        store_id = data['store_id']
        amount = data['amount']

        # Update sale details
        sale.product_quantity = product_quantity
        sale.store_id = store_id
        sale.amount = amount

        # Save to the database
        sale.save()

        return marshal(sale, sale_model), HTTPStatus.ACCEPTED

# Resource for deleting a sale by ID
@sales_namespace.route('/delete/<int:sale_id>')
class DeleteSaleResource(Resource):
    def delete(self, sale_id):
        sale = Sales.query.get(sale_id=sale_id)
        if sale:
            # Increase the product quantity
            product = Products.query.get(product_id=sale.product_id)
            product.quantity += sale.product_quantity

            # Delete the sale
            sale.delete()
            return {'message': 'Sale deleted successfully'}, HTTPStatus.NO_CONTENT
        return {'message': 'Sale not found'}, HTTPStatus.NOT_FOUND
