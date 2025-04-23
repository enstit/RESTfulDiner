# app/resources/auth.py

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource

from app.extensions import db
from app.models.user import User, UserRoleType


class ProtectedResource(Resource):
    @jwt_required()
    def authenticate(self, admin_only: bool = False) -> tuple[dict, int]:
        user_id = get_jwt_identity()
        claims = get_jwt()
        user = (
            db.session.query(User)
            .filter(User.user_id == user_id)
            .one_or_none()
        )
        if admin_only and user is not None and user.role != UserRoleType.ADMIN:
            return {"error": "Admin privileges required"}, 403
        return {
            "message": f"User {user_id} correctly authenticated in event {claims.get('event_id')}",
            "user_id": user_id,
            "event_id": claims.get("event_id"),
            "kiosk_id": claims.get("kiosk_id"),
        }, 200
