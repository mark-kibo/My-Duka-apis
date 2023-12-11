import pytest
from api.products import ProductsResource, product_parser, product_model
from api.models.products import Products

# Test product creation
def test_create_product():
    """
    Test that `create_product` creates a new product and returns it successfully.
    """

    resource = ProductsResource()
    new_product = {
        "product_name": "Test Product",
        "description": "This is a test product",
        "category": "Electronics",
        "brand": "Von",
        "quantity": 10,
        "buying_price": 8000,
        "selling_price": 9000,
        "payment_status": "Paid",
        "image_url": "https://naivas.online/101019-medium_default/von-subwoofer-21ch-ves1602fs.jpg",
        "store_id": 1,
        "supplier_id": 1,
    }

    response = resource.post(json=new_product)
    data = response.json

    assert response.status_code == 201
    assert data["product_name"] == "Test Product"
    assert data["description"] == "This is a test product"
    assert data["category"] == "Foodstuff"
    assert data["brand"] == "Avena"
    assert data["quantity"] == 10
    assert data["buying_price"] == 1200
    assert data["selling_price"] == 1299
    assert data["payment_status"] == "Paid"
    assert data["image_url"] == "https://naivas.online/103626-medium_default/avena-vegetable-oil-5l.jpg"
    assert data["store_id"] == 1
    assert data["supplier_id"] == 1

# Test getting a list of products
def test_get_products():
    """
    Test that `get_products` returns a list of all products.
    """

    resource = ProductsResource()
    response = resource.get()

    assert response.status_code == 200
    assert len(response.json["products"]) >= 1

# Test getting a specific product
def test_get_product():
    """
    Test that `get_product` returns the correct product for a valid ID.
    """

    resource = ProductsResource()
    product_id = 1  # Assuming a product exists with ID 1
    response = resource.get(product_id)

    assert response.status_code == 200
    assert response.json["product_id"] == product_id

# Test updating a product
def test_update_product():
    """
    Test that `update_product` updates the correct product for a valid ID.
    """

    resource = ProductsResource()
    product_id = 1  # Assuming a product exists with ID 1
    updated_data = {
        "product_name": "Updated Test Product",
        "quantity": 20,
    }

    response = resource.patch(product_id, json=updated_data)
    data = response.json

    assert response.status_code == 200
    assert data["product_name"] == "Updated Test Product"
    assert data["quantity"] == 20

# Test deleting a product
def test_delete_product():
    """
    Test that `delete_product` deletes the correct product for a valid ID.
    """

    resource = ProductsResource()
    product_id = 1  # Assuming a product exists with ID 1
    response = resource.delete(product_id)

    assert response.status_code == 200
    assert response.json["message"] == "Product deleted successfully"