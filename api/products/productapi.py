from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace, fields, marshal_with
from ..utils import db
from api.models.products import Products

api = Api()

# Namespace for Products
products_namespace = Namespace('products', description='products endpoints')

# Request parser for parsing JSON data in requests
product_parser = reqparse.RequestParser()
product_parser.add_argument('product_name', type=str, required=True, help='Product name is required')
product_parser.add_argument('description', type=str)
product_parser.add_argument('category', type=str)
product_parser.add_argument('brand', type=str)
product_parser.add_argument('quantity', type=int)
product_parser.add_argument('buying_price', type=int)
product_parser.add_argument('selling_price', type=int)
product_parser.add_argument('payment_status', type=str)
product_parser.add_argument('image_url', type=str)
product_parser.add_argument('store_id', type=int, required=True, help='Store ID is required')
product_parser.add_argument('supplier_id', type=int, required=True, help='Supplier ID is required')

# Model for serializing product data
product_model = api.model('Product', {
    'product_id': fields.Integer,
    'product_name': fields.String,
    'description': fields.String,
    'category': fields.String,
    'brand': fields.String,
    'quantity': fields.Integer,
    'buying_price': fields.Integer,
    'selling_price': fields.Integer,
    'payment_status': fields.String,
    'image_url': fields.String,
    'store_id': fields.Integer,
    'supplier_id': fields.Integer,
})

@products_namespace.route('/')
class ProductsResource(Resource):
    @api.doc('list_products')
    @marshal_with(product_model, envelope='products')
    def get(self):
        """
        Get a list of all products.
        """
        products = Products.query.all()
        return products

    @api.doc('create_product')
    @marshal_with(product_model)
    def post(self):
        """
        Create a new product.
        """
        args = product_parser.parse_args()
        new_product = Products(
            product_name=args['product_name'],
            description=args['description'],
            category=args['category'],
            brand=args['brand'],
            quantity=args['quantity'],
            buying_price=args['buying_price'],
            selling_price=args['selling_price'],
            payment_status=args['payment_status'],
            image_url=args['image_url'],
            store_id=args['store_id'],
            supplier_id=args['supplier_id'],
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

@products_namespace.route('/<int:product_id>')
class ProductResource(Resource):
    @api.doc('get_product')
    @marshal_with(product_model)
    def get(self, product_id):
        """
        Get details of a specific product.
        """
        product = Products.query.filter_by(product_id=product_id).first()
        return product

    @api.doc('update_product')
    @marshal_with(product_model)
    def patch(self, product_id):
        """
        Update details of a specific product.
        """
        args = product_parser.parse_args()
        product = Products.query.filter_by(product_id=product_id).first()

        product.product_name = args['product_name']
        product.description = args['description']
        product.category = args['category']
        product.brand = args['brand']
        product.quantity = args['quantity']
        product.buying_price = args['buying_price']
        product.selling_price = args['selling_price']
        product.payment_status = args['payment_status']
        product.image_url = args['image_url']
        product.store_id = args['store_id']
        product.supplier_id = args['supplier_id']

        db.session.commit()
        return product

    @api.doc('delete_product')
    def delete(self, product_id):
        """
        Delete a specific product.
        """
        product = Products.query.filter_by(product_id=product_id).first()
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}
