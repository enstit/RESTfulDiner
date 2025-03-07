# app/resources/DeliveryStation.py

from typing import Tuple

from flask_restful import reqparse

from app.dto.delivery_station import DeliveryStationDTO
from app.extensions import db
from app.models.delivery_station import DeliveryStation
from app.resources.auth import ProtectedResource


class DeliveryStationResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("active_flag", type=bool)

    def get(
        self, *, _id: str | None = None, name: str | None = None
    ) -> Tuple[dict, int]:
        if _id or name:
            delivery_station = (
                db.session.query(DeliveryStation)
                .where(
                    DeliveryStation.id == _id
                    if _id
                    else DeliveryStation.name == name
                )
                .one_or_none()
            )
            if delivery_station:
                return DeliveryStationDTO.from_model(delivery_station), 200
            return {"message": f"DeliveryStation {name} was not found"}, 404

        delivery_stations = db.session.query(DeliveryStation).all()
        return DeliveryStationDTO.from_model_list(delivery_stations), 200

    def post(self) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DeliveryStationResource.parser.parse_args()
        new_delivery_station = DeliveryStation(
            name=data["name"], active_flag=data["active_flag"]
        )
        db.session.add(new_delivery_station)
        db.session.commit()
        return DeliveryStationDTO.from_model(new_delivery_station), 201

    def put(self, _id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DeliveryStationResource.parser.parse_args()
        delivery_station = db.session.query(DeliveryStation).get(_id)
        if not delivery_station:
            return {"message": f"DeliveryStation {_id} was not found"}, 404
        delivery_station.name = data["name"]
        delivery_station.active_flag = data["active_flag"]

        db.session.commit()
        return DeliveryStationDTO.from_model(delivery_station), 200

    def patch(self, _id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DeliveryStationResource.parser.parse_args()
        delivery_station = db.session.query(DeliveryStation).get(_id)
        if not delivery_station:
            return {"message": f"DeliveryStation {_id} was not found"}, 404
        if "name" in data and data["name"]:
            delivery_station.name = data["name"]
        if "active_flag" in data:
            delivery_station.active_flag = data["active_flag"]

        db.session.commit()
        return DeliveryStationDTO.from_model(delivery_station), 200
