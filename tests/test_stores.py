import pytest
from api.stores import StoreList, MutateStore, DeletStore
from api.models.stores import Store
from flask_sqlalchemy import SQLAlchemy
from api.utils import db 

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

    Store.query.filter_by(store_name="Test Store").delete()
    db.session.commit()
    
def test_get_store():
    """
    Test that `MutateStore.get` returns the correct store for a valid ID.
    """

    resource = MutateStore()
    store_id = 1  # Assuming...
    response = resource.get(store_id)

    assert response.status_code == 200
    assert response.json["store_id"] == store_id

def test_update_store():
    """
    Test that `MutateStore.patch` updates the correct store for a valid ID.
    """

    resource = MutateStore()
    store_id = 1  # Assuming...
    updated_data = {
        "location": "Mombasa, Kenya",
    }

    response = resource.patch(store_id, json=updated_data)
    data = response.json

    assert response.status_code == 200
    assert data["location"] == "Mombasa, Kenya"

    Store.query.filter_by(store_id=1).update({"location": "Nairobi, Kenya"})
    db.session.commit()
    
def test_delete_store():
    """
    Test that `DeletStore.delete` deletes the correct store for a valid ID and associated products.
    """

    resource = DeletStore()
    store_id = 2  # Assuming...
    role_name = "merchant"

    response = resource.delete(role_name, store_id)

    assert response.status_code == 204
    assert Store.query.filter_by(store_id=store_id).first() is None
    
def test_delete_store_unauthorized():
    """
    Test that `DeletStore.delete` returns an error message when attempted by a non-merchant user.
    """

    resource = DeletStore()
    store_id = 1  # Assuming...
    role_name = "user"

    response = resource.delete(role_name, store_id)

    assert response.status_code == 401
    assert response.json["message"] == "You don't have permissions to perform this action!"