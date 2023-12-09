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