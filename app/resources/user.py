# app/resources/user.py

from flask_restful import Resource
from flask_restful import reqparse

from flask_jwt_extended import create_access_token

from app.extensions import db
from app.dto.user import UserDTO
from app.models.user import User
from app.models.user import UserRoleType


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("role", type=str, default=UserRoleType.OPERATOR.name)

    def get(
        self, *, _id: str | None = None, username: str | None = None
    ) -> tuple[dict, int]:
        if _id or username:
            user = (
                db.session.query(User)
                .where(User.id == _id if _id else User.username == username)
                .one_or_none()
            )
            if user:
                return UserDTO.from_model(user), 200
            return {"message": "User was not found"}, 404
        users = db.session.query(User).all()
        return UserDTO.from_model_list(users), 200

    def post(self) -> tuple[dict, int]:
        data = UserResource.parser.parse_args()
        new_user = User(
            username=data["username"],
            password=data["password"],
            role=UserRoleType[data["role"]],
        )
        db.session.add(new_user)
        db.session.commit()
        return UserDTO.from_model(new_user), 201

    @staticmethod
    def authenticate(username: str, password: str) -> User | None:
        user = (
            db.session.query(User)
            .where(User.username == username)
            .one_or_none()
        )
        if user and user.password == password:
            return user
        return None


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Username cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password cannot be blank"
    )

    def post(self) -> tuple[dict, int]:
        data = LoginResource.parser.parse_args()
        user = UserResource.authenticate(data["username"], data["password"])

        if not user:
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(
            identity=user.id, additional_claims={"role": user.role}
        )
        return {"access_token": access_token}, 200
