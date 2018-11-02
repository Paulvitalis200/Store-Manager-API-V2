from flask import Blueprint
from flask_restful import Api

from .views.products import Products
from .views.users import UserRegistration

my_apis = Blueprint("resources.api", __name__, url_prefix='/api/v2')
api = Api(my_apis)

api.add_resource(
    Products,
    "/products",
    endpoint="products"
)

api.add_resource(
    Products,
    "/products/<int:id>",
    endpoint="update"
)

api.add_resource(
    UserRegistration,
    "/register",
    endpoint="register"
)
