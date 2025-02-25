from flask_restful import Resource, reqparse
from app.models.user import User
from app.dto.user import UserDTO
from app.database import db


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Username cannot be blank"
    )

    def get(self, name):
        user = (
            db.session.query(User).where(User.username == name).one_or_none()
        )
        if user:
            return UserDTO.from_model(user), 200
        return {"message": "User not found"}, 404

    def post(self):
        data = UserResource.parser.parse_args()
        new_user = User(username=data["username"])
        db.session.add(new_user)
        db.session.commit()
        return UserDTO.from_model(new_user), 201
