# app/resources/user.py

from datetime import datetime

from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse, request

from app.dto.user import UserDTO
from app.extensions import db
from app.models.cfg_user import CfgUser, UserRoleType
from app.models.cfg_event import CfgEvent
from app.models.cfg_event_day import CfgEventDay
from app.models.cfg_kiosk import CfgKiosk
from app.models.sys_shift import SysShift
from app.resources.auth import ProtectedResource


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
                db.session.query(CfgUser)
                .filter(CfgUser.user_id == user_id)
                .one_or_none()
            )
            if user:
                return UserDTO.from_model(user), 200
            return {"error": f"User {user_id} was not found"}, 404
        users = db.session.query(CfgUser).all()
        return UserDTO.from_model_list(users), 200

    def post(self) -> tuple[dict, int]:
        data = UserResource.parser.parse_args()
        new_user = CfgUser(
            username=data["username"],
            password=data["password"],
            role=UserRoleType[data["role"]],
        )
        db.session.add(new_user)
        db.session.commit()
        return UserDTO.from_model(new_user), 201

    @staticmethod
    def authenticate(user_id: str, password: str) -> CfgUser | None:
        user = (
            db.session.query(CfgUser)
            .filter(CfgUser.user_id == user_id)
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
                db.session.query(CfgEvent)
                .filter(CfgEvent.event_id == event_id)
                .one_or_none()
            )
        ):
            return {"error": f"Event {event_id} was not found"}, 404

        # Check if there exist a kiosk in the event with the given kiosk_id
        kiosk = (
            db.session.query(CfgKiosk)
            .filter(
                CfgKiosk.event_id == event_id, CfgKiosk.kiosk_id == kiosk_id
            )
            .one_or_none()
        )

        # Check if the user is already logged in for the event
        if (
            db.session.query(SysShift)
            .filter(
                SysShift.event_id == event_id,
                SysShift.user == user,
                SysShift.logout_datetime == None,
            )
            .one_or_none()
        ):
            return {
                "error": f"User {user_id} is already logged in for event {event_id}"
            }, 400

        # For the user and event combination, return an access token to be used
        # for authentication in subsequent requests
        access_token = create_access_token(
            identity=user.user_id,
            additional_claims={
                "event_id": event.event_id,
                "kiosk_id": kiosk.kiosk_id if kiosk else None,
            },
        )

        # Create a new SysShift object and add it to the database
        new_shift = SysShift(event=event, user=user, token=access_token)
        db.session.add(new_shift)
        db.session.commit()

        return {"access_token": access_token}, 200


class LogoutResource(ProtectedResource):
    parser = reqparse.RequestParser()

    def post(self, user_id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        event_id = msg.get("event_id")

        # Check if the user exists and is active
        if not (
            user := db.session.query(CfgUser)
            .filter(CfgUser.user_id == user_id)
            .one_or_none()
        ):
            return {
                "error": f"Invalid credentials provided for user with ID {user_id}"
            }, 401
        # Recover the SyShift object for the user that is still logged in
        if shift := (
            db.session.query(SysShift)
            .filter(
                SysShift.event_id == event_id,
                SysShift.user == user,
                SysShift.logout_datetime == None,
            )
            .one_or_none()
        ):
            # Create a new SysShift object and add it to the database
            shift.logout_datetime = datetime.now()
            db.session.add(shift)
            db.session.commit()

            return {
                "message": f"User {user_id} successfully logged out from event {event_id}"
            }, 200
        return {
            "error": f"User {user_id} is not logged in in the event {event_id}, or was not found"
        }, 404
