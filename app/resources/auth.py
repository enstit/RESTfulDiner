# app/resources/auth.py

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models.user import User
from app.models.user import UserRoleType


class ProtectedResource(Resource):
    @jwt_required()
    def authenticate(self, admin_only: bool = False) -> tuple[dict, int]:
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).one_or_none()
        if admin_only and user.role != UserRoleType.ADMIN:
            return {"message": "Admin privileges required"}, 403
        return {"message": f"Hello, user {user_id}"}, 200
