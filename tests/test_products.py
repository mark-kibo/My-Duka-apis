import pytest
from .products import ProductsResource, product_parser, product_model


@pytest.mark.parametrize("product_name, description, expected_response", [
    ("Test Product 1", "This is a test product.", 200),
    ("Test Product 2", "Another test product.", 200),
])
def test_get_products(product_name, description, expected_response):
    """
    Test that `get_products` returns a list of all products.
    """
    with pytest.mock.patch.object(Products, "query"):
        Products.query.all.return_value = [
            Products(product_id=1, product_name=product_name, description=description),
            Products(product_id=2, product_name="Another Product", description="Another description"),
        ]

        resource = ProductsResource()
        response = resource.get()

        assert response.status_code == expected_response
        assert len(response.json["products"]) == 2
        assert response.json["products"][0]["product_name"] == product_name
        assert response.json["products"][0]["description"] == description


def test_get_product_valid_id():
    """
    Test that `get_product` returns the correct product details for a valid ID.
    """
    with pytest.mock.patch.object(Products, "query"):
        Products.query.filter_by.return_value.first.return_value = Products(
            product_id=1, product_name="Test Product", description="This is a test product."
        )

        resource = ProductsResource()
        response = resource.get(1)

        assert response.status_code == 200
        assert response.json["product_id"] == 1
        assert response.json["product_name"] == "Test Product"
        assert response.json["description"] == "This is a test product."


def test_get_product_invalid_id():
    """
    Test that `get_product` returns a 404 error for an invalid ID.
    """
    with pytest.mock.patch.object(Products, "query"):
        Products.query.filter_by.return_value.first.return_value = None

        resource = ProductsResource()
        response = resource.get(999)

        assert response.status_code == 404
        assert response.json["message"] == "Product not found"


def test_create_product():
    """
    Test that `create_product` creates a new product and returns it successfully.
    """
    with pytest.mock.patch.object(Products, "save"):
        resource = ProductsResource()
        response = resource.post(
            json={
                "product_name": "New Product",
                "description": "This is a new product.",
                "category": "Foodstuff",
                "brand": "Avena",
                "quantity": 10,
                "buying_price": 1200,
                "selling_price": 1299,
                "payment_status": "paid",
                "image_url": "https://naivas.online/103626-medium_default/avena-vegetable-oil-5l.jpg",
                "store_id": 1,
                "supplier_id": 2,
            }
        )

        assert response.status_code == 201
        assert response.json["product_name"] == "New Product"
        assert response.json["description"] == "This is a new product."
