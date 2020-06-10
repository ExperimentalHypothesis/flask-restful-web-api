from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# custom imports
from security import authenticate, identify
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

# initializing main app
app = Flask(__name__)
app.secret_key = "sadaddaf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# initializing app extension
api = Api(app)
jwt = JWT(app, authenticate, identify) # JWT create a new endpoint /auth 

# creating api endpoints
api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>") 
api.add_resource(Items, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")


if __name__ == "__main__":
    # to avoid circular imports
    from db import db
    db.init_app(app)
    app.run(debug=True)
