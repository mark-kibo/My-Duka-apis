import pytest




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

