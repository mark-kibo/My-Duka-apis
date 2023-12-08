import pytest




@pytest.mark.parametrize("product_name, description, expected_response", [
    ("Test Product 1", "This is a test product.", 200),
    ("Test Product 2", "Another test product.", 200),
])
def test_get_products(product_name, description, expected_response):
    """
    Test that `get_products` returns a list of all products.
    """
    
