import pytest
from api.stores.views import StoreList, MutateStore, DeletStore
from api.models.stores import Store

def test_get_all_stores():
    """
    Test that `StoreList.get` returns a list of all stores.
    """

    resource = StoreList()
    response = resource.get()

    assert response.status_code == 200
    assert len(response.json) >= 0
    
def test_create_store():
    """
    Test that `StoreList.post` creates a new store and returns it successfully.
    """

    resource = StoreList()
    new_store = {
        "store_name": "Test Store",
        "location": "Nairobi, Kenya",
    }

    response = resource.post(json=new_store)
    data = response.json

    assert response.status_code == 201
    assert data["store_name"] == "Test Store"
    assert data["location"] == "Nairobi, Kenya"

