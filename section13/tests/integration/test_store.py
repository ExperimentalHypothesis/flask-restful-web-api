from models.store import StoreModel
from models.item import ItemModel

import pytest
from app import app
from db import db


@pytest.fixture(autouse=True)
def test_client_db():

    # set up
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    with app.app_context():
        db.init_app(app)
        db.create_all()
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    # do testing
    yield testing_client

    # tear down
    with app.app_context():
        db.session.remove()
        db.drop_all()

    ctx.pop()


def test_json(test_client_db):
    store = StoreModel("test")
    store.save_to_db()
    expected = {
            "id": 1,
            "name": "test",
            "items": [],
        }
    assert expected == store.json()

    # nonempty
    store1 = StoreModel("testing")
    store1.save_to_db()
    item1 = ItemModel("one", 10, 2)
    item2 = ItemModel("two", 10, 2)
    item1.save_to_db()
    item2.save_to_db()
    expected = {
            "id": 2,
            "name": "testing",
            "items": [
                {
                    "id": 1,
                    "name": "one",
                    "price": 10,
                    "store_id": 2,
                },
                {
                    "id": 2,
                    "name": "two",
                    "price": 10,
                    "store_id": 2,
                },
            ],
        }
    assert expected == store1.json()


def test_find_by_name(test_client_db):
    store = StoreModel("first")
    store.save_to_db()

    found = StoreModel.find_by_name("first")
    assert found.name == "first"
    assert found.id == 1
    assert list(found.items) == []

    store = StoreModel("second")
    store.save_to_db()
    i1 = ItemModel("test", 10, 2)
    i2 = ItemModel("testing", 11, 2)
    i1.save_to_db()
    i2.save_to_db()
    found = StoreModel.find_by_name("second")
    assert found.name == "second"
    assert found.id == 2
    assert len(list(found.items)) == 2
    # assert found.items == [
    #     {
    #         "id": 1,
    #         "name": "test",
    #         "price": 10,
    #         "store_id": 2,
    #     },
    #     {
    #         "id": 2,
    #         "name": "testing",
    #         "price": 11,
    #         "store_id": 2,
    #     }
    # ]


def test_find_all(test_client_db):
    s1 = StoreModel("first")
    s2 = StoreModel("second")
    s3 = StoreModel("third")
    s1.save_to_db()
    s2.save_to_db()
    s3.save_to_db()
    assert len(StoreModel.find_all()) == 3


def test_save_delete(test_client_db):
    s = StoreModel("test")
    found = StoreModel.find_by_name("test")
    assert found is None

    s.save_to_db()
    found = StoreModel.find_by_name("test")
    assert found is not None
    assert found.id == 1
    assert found.name == "test"

    s.delete_from_db()
    found = StoreModel.find_by_name("test")
    assert found is None


