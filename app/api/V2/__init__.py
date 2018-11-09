from flask import Blueprint
from flask_restful import Api

from .views.products import Products, SingleProduct
from .views.users import (UserRegistration, UserLogin, UserLogout,
                          GetAllUsers, GetEachUser)
from .views.sales import Sales, SingleSale

my_apis = Blueprint("resources.api", __name__, url_prefix='/api/v2')
api = Api(my_apis)

api.add_resource(
    Products,
    "/products",
    endpoint="products"
)

api.add_resource(
    SingleProduct,
    "/products/<int:id>"
)

api.add_resource(
    UserRegistration,
    "/auth/signup",
    endpoint="signup"
)

api.add_resource(
    UserLogin,
    "/auth/login",
    endpoint="login"
)

api.add_resource(
    UserLogout,
    "/auth/logout",
    endpoint="logout"
)

api.add_resource(
    Sales,
    "/sales",
    endpoint="sales"
)

api.add_resource(
    SingleSale,
    "/sales/<int:id>",
    endpoint="sale"
)

api.add_resource(
    GetAllUsers,
    "/users",
    endpoint="users"
)

api.add_resource(
    GetEachUser,
    "/users/<int:id>",
    endpoint="user"
)
