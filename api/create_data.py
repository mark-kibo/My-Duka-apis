# Create dummy data

from .models.receipts import Receipts
from .models.sales import Sales
from .models.stores import Store
from .models.products import Products
from .models.suppliers import Suppliers
from .models.supplyrequests import SupplyRequests
from .models.users import User
from faker import Faker
from runserver import app
from .utils import db










fake = Faker()



with app.app_context():
    


    def generate_fake_data():
        # Create a SQLAlchemy database connection
        db.create_all()

        # Generate fake users
        users = []
        for _ in range(2):
            user = User(
                username=fake.user_name(),
                password=fake.password(),
                email=fake.email(),
                full_name=fake.name(),
                role=fake.random_element(elements=('merchant','admin', 'clerk')),
                store_id=fake.random_element(elements=stores).store_id
            )
            users.append(user)

        

        # Generate fake suppliers
        suppliers = []
        for _ in range(3):
            supplier = Suppliers(
                supply_name=fake.company(),
                supplier_contact=fake.phone_number(),
                supplier_email=fake.email(),
                supplier_address=fake.address(),
            )
            suppliers.append(supplier)

        db.session.add_all(suppliers)
        db.session.commit()

        # Generate fake stores
        stores = []
        for _ in range(2):
            store = Store(
                user_id=fake.random_element(elements=users).user_id,
                supplier_id=fake.random_element(elements=suppliers).supplier_id,
                location=fake.address(),
            )
            stores.append(store)

        db.session.add_all(stores)
        db.session.commit()

        # Generate fake products
        products = []
        for _ in range(10):
            product = Products(
                product_name=fake.word(),
                description=fake.sentence(),
                category=fake.random_element(elements=('Electronics', 'Clothing', 'Books')),
                brand=fake.word(),
                quantity=fake.random_int(min=1, max=100),
                buying_price=fake.random_int(min=10, max=100),
                selling_price=fake.random_int(min=20, max=150),
                payment_status=fake.random_element(elements=('Pending', 'Paid')),
                image_url=fake.image_url(),
                store_id=fake.random_element(elements=stores).store_id,
                supplier_id=fake.random_element(elements=suppliers).supplier_id,
            )
            products.append(product)

        db.session.add_all(products)
        db.session.commit()

        # Generate fake supply requests
        supply_requests = []
        for _ in range(5):
            request = SupplyRequests(
                clerk_id=fake.random_element(elements=users).user_id,
                product_id=fake.random_element(elements=products).product_id,
                quantity_requested=fake.random_int(min=1, max=20),
                reason_for_request=fake.sentence(),
                received_items=fake.random_int(min=0, max=10),
                received=fake.random_element(elements=(True, False)),
                approved=fake.random_element(elements=(True, False)),
            )
            supply_requests.append(request)

        db.session.add_all(supply_requests)
        db.session.commit()

        # Generate fake receipts
        receipts = []
        for _ in range(5):
            receipt = Receipts(
                date_time=fake.date_time(),
                product_id=fake.random_element(elements=products).product_id,
                quantity_received=fake.random_int(min=1, max=20),
                payment_status=fake.random_element(elements=('Pending', 'Paid')),
            )
            receipts.append(receipt)

        db.session.add_all(receipts)
        db.session.commit()

        # Generate fake sales
        sales = []
        for _ in range(5):
            sale = Sales(
                product_id=fake.random_element(elements=products).product_id,
                product_quantity=fake.random_int(min=1, max=10),
                store_id=fake.random_element(elements=stores).store_id,
                amount=fake.random_int(min=50, max=200),
            )
            sales.append(sale)

        db.session.add_all(sales)
        db.session.commit()

        # Close the database connection
        db.session.close()

    if __name__ == "__main__":
        generate_fake_data()