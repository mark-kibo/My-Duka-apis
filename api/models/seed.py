# Create dummy data
from ..utils import db
from .receipts import Receipts
from .sales import Sales
from .stores import Store
from .products import Products
from .suppliers import Suppliers
from .supplyrequests import SupplyRequests
from .users import User
from faker import Faker
from runserver import app


from datetime import datetime

from random import randint
from flask_sqlalchemy import SQLAlchemy
from runserver import create_app




fake = Faker()

def seed_users():
    
    stores = Store.query.all()

    for _ in range(5):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            full_name=fake.name(),
            role=fake.random_element(elements=('merchant', 'admin', 'clerk')),
            store_id=stores[randint(0, len(stores) - 1)].store_id  
        )
        db.session.add(user)

    db.session.commit()

def seed_suppliers():
    existing_supplier_ids = [supplier.supplier_id for supplier in Suppliers.query.all()]
    for i in range(1, 3):
        while i in existing_supplier_ids:
            i += 1
        supplier = Suppliers(
            supplier_id=i,
            supply_name=fake.company(),
            supplier_contact=fake.phone_number(),
            supplier_email=fake.email(),
            supplier_address=fake.address()
        )
        db.session.add(supplier)
        existing_supplier_ids.append(i)
    db.session.commit()

def seed_stores():
    users = User.query.filter_by(role='clerk').limit(5).all()  
    suppliers = Suppliers.query.all()

    for user in users:
        store = Store(
            user=user,
            supplier_id=randint(1, len(suppliers)),
            location=fake.address()
        )
        db.session.add(store)

    db.session.commit()


def seed_products():
    stores = Store.query.all()
    suppliers = Suppliers.query.all()

    for _ in range(10):
        product = Products(
            product_name=fake.word(),
            description=fake.text().replace('\n', ' '),  
            category=fake.word(),
            brand=fake.company(),
            quantity=randint(1, 100),
            buying_price=randint(10, 100),
            selling_price=randint(50, 200),
            payment_status='unpaid',
            image_url=fake.image_url(),
            store_id=stores[randint(0, len(stores) - 1)].store_id,
            supplier=suppliers[randint(0, len(suppliers) - 1)]
        )
        db.session.add(product)

    
    db.session.commit()

    
    seeded_products = Products.query.all()
    for product in seeded_products:
        print(
            f"{product.product_id} | {product.product_name} | {product.description} | {product.category} | {product.brand} | "
            f"{product.quantity} | {product.buying_price} | {product.selling_price} | {product.payment_status} | "
            f"{product.image_url} | {product.store_id} | {product.supplier_id}"
        )


def seed_receipts():
    products = Products.query.all()

    for product in products:
        payment_status = fake.random_element(elements=('paid', 'unpaid'))
        receipt = Receipts(
            date_time=datetime.now(),
            product=product,
            quantity_received=randint(1, 20),
            payment_status=payment_status
        )
        db.session.add(receipt)

    db.session.commit()

def seed_sales():
    products = Products.query.all()
    stores = Store.query.all()

    for _ in range(5):
        sale = Sales(
            product_id=products[randint(0, len(products) - 1)].product_id,  
            product_quantity=randint(1, 10),
            store_id=stores[randint(0, len(stores) - 1)].store_id,
            amount=randint(50, 500)
        )
        db.session.add(sale)

def seed_supply_requests():
    clerks = User.query.filter_by(role='clerk').all()
    products = Products.query.all()

    for clerk in clerks:
        request = SupplyRequests(
            clerk_id=clerk.user_id,  
            product_id=products[randint(0, len(products) - 1)].product_id,
            quantity_requested=randint(5, 30),
            reason_for_request=fake.sentence(),
            received_items=randint(1, 10),
            received=True,
            approved=True
        )
        db.session.add(request)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_users()
        seed_suppliers() 
        seed_stores()
        seed_products()
        seed_receipts()
        seed_sales()
        seed_supply_requests()
        db.session.commit()
