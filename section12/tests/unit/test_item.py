from models.item import ItemModel


def test_item_init():
    item = ItemModel("test", 19.99, 1)
    assert item.name == "test"
    assert item.store_id == 1
    assert item.price == 19.99


def test_repr():
    item = ItemModel("test", 19.99, 1)
    expected = "<Itemmodel test, 19.99>"
    assert expected == item.__repr__()


