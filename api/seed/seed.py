from faker import Faker
from random import randint, choice
from datetime import datetime
from ..models.users import User
from ..models.products import Products
from ..models.receipts import Receipts
from ..models.sales import Sales
from ..models.stores import Store
from ..models.suppliers import Suppliers
from ..models.supplyrequests import SupplyRequests
from api import create_app


app = create_app()
with app.app_context():
    fake = Faker()

        # Create fake users
    for _ in range(50):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            full_name=fake.name(),
            role=choice(['admin', 'manager', 'employee']),
            store_id=choice(Store.query.all()).store_id,
        )
        user.save()

    # Create fake suppliers
    for _ in range(20):
        supplier = Suppliers(
            supply_name=fake.company(),
            supplier_contact=fake.phone_number(),
            supplier_email=fake.email(),
            supplier_address=fake.address(),
        )
        supplier.save()

    # Create fake stores
    for _ in range(5):
        store = Store(
            store_name=fake.company(),
            location=fake.address(),
        )
        store.save()

        # Assign random products to the store
    for _ in range(randint(5, 10)):
        product = Products(
                product_name=fake.word(),
                description=fake.text(),
                category=choice(['Electronics', 'Clothing', 'Books', 'Toys']),
                brand=fake.company(),
                quantity=randint(10, 100),
                buying_price=randint(10, 100),
                selling_price=randint(100, 200),
                payment_status=choice(['Paid', 'Pending']),
                image_url=fake.image_url(),
                store_id=store.store_id,
                supplier_id=choice(Suppliers.query.all()).supplier_id,
            )
        product.save()

            # Create fake supply requests for the product
    for _ in range(randint(1, 5)):
        supply_request = SupplyRequests(
                users_id=choice(User.query.all()).user_id,
                product_id=product.product_id,
                quantity_requested=randint(1, 20),
                reason_for_request=fake.sentence(),
                received_items=randint(1, 20),
                received=choice([True, False]),
                approved=choice([True, False]),
                )
        supply_request.save()

    # Create fake receipts
    for _ in range(20):
        receipt = Receipts(
            date_time=fake.date_time(),
            product_id=choice(Products.query.all()).product_id,
            quantity_received=randint(1, 20),
            payment_status=choice(['Paid', 'Pending']),
        )
        receipt.save()

    # Create fake sales
    for _ in range(30):
        sale = Sales(
            product_id=choice(Products.query.all()).product_id,
            product_quantity=randint(1, 10),
            store_id=choice(Store.query.all()).store_id,
            amount=randint(50, 200),
        )
        sale.save()
