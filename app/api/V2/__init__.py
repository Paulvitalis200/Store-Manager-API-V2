from flask import Blueprint
from flask_restful import Api

from .views.products import Products, SingleProduct
from .views.users import UserRegistration, UserLogin, UserLogout
from .views.sales import Sales, SingleSaleAdmin

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
    "/register",
    endpoint="register"
)

api.add_resource(
    UserLogin,
    "/login",
    endpoint="login"
)

api.add_resource(
    UserLogout,
    "/logout",
    endpoint="logout"
)

api.add_resource(
    Sales,
    "/sales",
    endpoint="sales"
)

api.add_resource(
    SingleSaleAdmin,
    "/sales/<int:id>",
    endpoint="sale"
)

