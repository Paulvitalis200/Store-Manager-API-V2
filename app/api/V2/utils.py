from .models import UserModel
from flask_jwt_extended import get_jwt_identity


def admin_only():
    user = UserModel.find_by_email(get_jwt_identity())
    if user[4] != "admin":
        return {
            "message": "You do not have authorization to access this feature"
        }
