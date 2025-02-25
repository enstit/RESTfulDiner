# app/resources/user.py

from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import request

from app.database import db
from app.dto.user import UserDTO
from app.models.user import User
from app.models.user import UserRoleType


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Username of the user"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password for the user"
    )
    parser.add_argument(
        "role",
        type=str,
        required=False,
        choices=[role.name for role in UserRoleType],
        default=UserRoleType.OPERATOR.name,
        help="Role of the user in the system",
    )

    def get(self):
        id = request.args.get("id")
        username = request.args.get("username")
        if id or username:
            user = (
                db.session.query(User)
                .where(User.id == id if id else User.username == username)
                .one_or_none()
            )
            if user:
                return UserDTO.from_model(user), 200
            return {"message": f"User {username} was not found"}, 404
        users = db.session.query(User).all()
        return UserDTO.from_model_list(users), 200

    def post(self):
        data = UserResource.parser.parse_args()
        new_user = User(
            username=data["username"],
            password=data["password"],
            role=UserRoleType[data["role"]],
        )
        db.session.add(new_user)
        db.session.commit()
        return UserDTO.from_model(new_user), 201
