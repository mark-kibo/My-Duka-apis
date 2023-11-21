# Create dummy data
from api.models.product import Products
from api.models.receipts import Receipts
from api.models.sales import Sales
from api.models.store import Store
from api.models.supplier import Suppliers
from api.models.supplyRequest import SupplyRequests
from api.models.users import Users
from .utils import db

def create_dummy_data():
    # Users
    user1 = Users(username="john_doe", password="password1", email="john@example.com", full_name="John Doe", role="superuser")
    user2 = Users(username="jane_doe", password="password2", email="jane@example.com", full_name="Jane Doe", role="admin")
    user3 = Users(username="bob_smith", password="password3", email="bob@example.com", full_name="Bob Smith", role="data entry clerk")
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Products
    product1 = Products(product_name="Laptop", description="High-performance laptop", category="Electronics", brand="ABC", quantity=50, buying_price=800.0, selling_price=1200.0, payment_status="unpaid", image_url="laptop_image.jpg")
    product2 = Products(product_name="Smartphone", description="Latest smartphone model", category="Electronics", brand="XYZ", quantity=100, buying_price=500.0, selling_price=800.0, payment_status="paid", image_url="smartphone_image.jpg")
    db.session.add_all([product1, product2])
    db.session.commit()

    # Receipts
    receipt1 = Receipts(product_id=1, quantity_received=10, payment_status="unpaid")
    receipt2 = Receipts(product_id=2, quantity_received=20, payment_status="paid")
    db.session.add_all([receipt1, receipt2])
    db.session.commit()

    # Supply Requests
    request1 = SupplyRequests(clerk_id=3, product_id=1, quantity_requested=30, reason_for_request="Low stock")
    request2 = SupplyRequests(clerk_id=3, product_id=2, quantity_requested=50, reason_for_request="New product launch")
    db.session.add_all([request1, request2])
    db.session.commit()

    # Store
    store1 = Store(user_id=1, location="Main Street", product_id=1, supplier_id=1)
    store2 = Store(user_id=2, location="Downtown", product_id=2, supplier_id=2)
   

    db.session.add_all([store1, store2])
    db.session.commit()

    # Suppliers
    supplier1 = Suppliers(supply_name="Supplier1", supplier_contact="Contact1", supplier_email="supplier1@example.com", supplier_address="Address1", product_id=1, store_id=1)
    supplier2 = Suppliers(supply_name="Supplier2", supplier_contact="Contact2", supplier_email="supplier2@example.com", supplier_address="Address2", product_id=2, store_id=2)
    db.session.add_all([supplier1, supplier2])
    db.session.commit()

    # Sales
    sale1 = Sales(product_id=1, product_quantity=5, store_id=1, amount=1500.0)
    sale2 = Sales(product_id=2, product_quantity=10, store_id=2, amount=8000.0)
    db.session.add_all([sale1, sale2])
    db.session.commit()


create_dummy_data()