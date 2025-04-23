# app/resources/user.py

from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse, request

from app.dto.user import UserDTO
from app.extensions import db
from app.models.user import User, UserRoleType
from app.models.event import Event
from app.models.kiosk import Kiosk


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("role", type=str, default=UserRoleType.OPERATOR.name)

    def get(
        self, *, user_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        if user_id:
            user = (
                db.session.query(User)
                .filter(User.user_id == user_id)
                .one_or_none()
            )
            if user:
                return UserDTO.from_model(user), 200
            return {"error": f"User {user_id} was not found"}, 404
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
    def authenticate(user_id: str, password: str) -> User | None:
        user = (
            db.session.query(User)
            .filter(User.user_id == user_id)
            .one_or_none()
        )
        if user and user.password == password:
            return user
        return None


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "password", type=str, required=True, help="Password cannot be blank"
    )

    def post(self, user_id: str) -> tuple[dict, int]:
        # Parse the `event_id` and `kiosk_id`arguments from the query string
        event_id = request.args.get("event_id", type=str)
        kiosk_id = request.args.get("kiosk_id", type=str)
        # Parse the `password` argument from the POST body
        password = LoginResource.parser.parse_args()["password"]

        # Check if the user exists and is active
        if not (user := UserResource.authenticate(user_id, password)):
            return {
                "error": f"Invalid credentials provided for user with ID {user_id}"
            }, 401

        # Check if there exists an event with the given event_id
        if not (
            event := (
                db.session.query(Event)
                .filter(Event.event_id == event_id)
                .one_or_none()
            )
        ):
            return {"error": f"Event {event_id} was not found"}, 404

        # Check if there exist a kiosk in the event with the given kiosk_id
        kiosk = (
            db.session.query(Kiosk)
            .filter(Kiosk.event_id == event_id, Kiosk.kiosk_id == kiosk_id)
            .one_or_none()
        )

        # For the user and event combination, return an access token to be used
        # for authentication in subsequent requests
        access_token = create_access_token(
            identity=user.user_id,
            additional_claims={
                "event_id": event.event_id,
                "kiosk_id": kiosk.kiosk_id if kiosk else None,
            },
        )
        return {"access_token": access_token}, 200
