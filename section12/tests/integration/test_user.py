from models.user import UserModel

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
    u = UserModel("test", "passtest")
    u.save_to_db()
    expected = {"id": 1, "username": "test"}
    assert expected == u.json()


def test_save_delete(test_client_db):
    u = UserModel("test", "passtest")
    found_by_id = u.get_user_by_id(1)
    assert found_by_id is None

    u.save_to_db()
    found_by_id = u.get_user_by_id(1)
    assert found_by_id is not None

    u.delete_from_db()
    found_by_id = u.get_user_by_id(1)
    assert found_by_id is None


def test_get_user_by_id(test_client_db):
    u = UserModel("test", "passtest")
    u.save_to_db()
    found_by_id = u.get_user_by_id(1)
    assert found_by_id.username == "test"
    assert found_by_id.password == "passtest"
    assert found_by_id.id == 1

