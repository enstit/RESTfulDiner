# app/resources/delivery_station.py

from flask_restful import reqparse

from app.dto.delivery_station import DeliveryStationDTO
from app.extensions import db
from app.models.cfg_delivery_station import CfgDeliveryStation
from app.resources.auth import ProtectedResource


class DeliveryStationResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("active_flag", type=bool)

    def get(
        self, *, delivery_station_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if delivery_station_id:
            delivery_station = (
                db.session.query(CfgDeliveryStation)
                .filter(
                    CfgDeliveryStation.event_id == msg.get("event_id"),
                    CfgDeliveryStation.delivery_station_id
                    == delivery_station_id,
                )
                .one_or_none()
            )
            if delivery_station:
                return DeliveryStationDTO.from_model(delivery_station), 200
            return {
                "error": f"DeliveryStation {delivery_station_id} was not found in the current event"
            }, 404

        delivery_stations = (
            db.session.query(CfgDeliveryStation)
            .filter(CfgDeliveryStation.event_id == msg.get("event_id"))
            .all()
        )
        return DeliveryStationDTO.from_model_list(delivery_stations), 200

    def post(self) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DeliveryStationResource.parser.parse_args()
        new_delivery_station = CfgDeliveryStation(
            event_id=msg.get("event_id"),
            name=data["name"],
            active_flag=data["active_flag"],
        )
        db.session.add(new_delivery_station)
        db.session.commit()
        return DeliveryStationDTO.from_model(new_delivery_station), 201

    def put(self, delivery_station_id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DeliveryStationResource.parser.parse_args()
        delivery_station = (
            db.session.query(CfgDeliveryStation)
            .filter(
                CfgDeliveryStation.event_id == msg.get("event_id"),
                CfgDeliveryStation.delivery_station_id == delivery_station_id,
            )
            .one_or_none()
        )
        if not delivery_station:
            return {
                "error": f"DeliveryStation {delivery_station_id} was not found in the current event"
            }, 404
        delivery_station.name = data["name"]
        delivery_station.active_flag = data["active_flag"]

        db.session.commit()
        return DeliveryStationDTO.from_model(delivery_station), 200

    def patch(self, delivery_station_id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DeliveryStationResource.parser.parse_args()
        delivery_station = (
            db.session.query(CfgDeliveryStation)
            .filter(
                CfgDeliveryStation.event_id == msg.get("event_id"),
                CfgDeliveryStation.delivery_station_id == delivery_station_id,
            )
            .one_or_none()
        )
        if not delivery_station:
            return {
                "error": f"DeliveryStation {delivery_station_id} was not found in the current event"
            }, 404
        if "name" in data and data["name"]:
            delivery_station.name = data["name"]
        if "active_flag" in data:
            delivery_station.active_flag = data["active_flag"]

        db.session.commit()
        return DeliveryStationDTO.from_model(delivery_station), 200
