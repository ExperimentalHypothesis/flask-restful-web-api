from ma import ma
from models.user import UserModel


class UserSchema(ma.Schema):
    """ Schema for dump/load user model. """

    class Meta:
        model = UserModel  # flask-marmallow will no create object directly based on the database schema
        fields = ("username", "password", "id")
        load_only = (
            "password",
        )  # thle jenom prijimat ale nikdy neposilat ven jako dzejson
        dump_only = ("id",)  # tohle neni potreba davat to prida sqlalch
