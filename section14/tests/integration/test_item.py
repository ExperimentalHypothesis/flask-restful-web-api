from models.item import ItemModel


def test_find_by_name(test_client_db):
    item = ItemModel(name="test", price=19.99, store_id=1)
    item.save_to_db()
    found = ItemModel.find_item_by_name("test")
    assert found.name == item.name
    assert found.price == item.price
    assert found.store_id == item.store_id
    assert found.id == item.id


def test_find_all(test_client_db):
    first = ItemModel(name="first", price=1.09, store_id=1)
    second = ItemModel(name="second", price=2.09, store_id=1)
    first.save_to_db()
    second.save_to_db()
    qry_res = ItemModel.find_all()
    assert len(qry_res) == 2


def test_save_delete(test_client_db):
    one = ItemModel(name="one", price=1.99, store_id=1)

    found = ItemModel.find_item_by_name("one")
    assert found is None

    one.save_to_db()
    found = ItemModel.find_item_by_name("one")
    assert found is not None

    one.delete_from_db()
    found = ItemModel.find_item_by_name("one")
    assert found is None
