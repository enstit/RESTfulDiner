# app/dto/delivery_station.py


from typing import List

from app.config import Config
from app.models.cfg_delivery_station import CfgDeliveryStation


class DeliveryStationDTO:
    def __init__(self, delivery_station: CfgDeliveryStation):
        self.event_id = str(delivery_station.event_id)
        self.delivery_station_id = str(delivery_station.delivery_station_id)
        self.name = delivery_station.name
        self.is_active = delivery_station.active_flag

    def to_dict(self) -> dict:
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/delivery_stations/{self.delivery_station_id}",
            "id": self.delivery_station_id,
            "name": self.name,
            "is_active": self.is_active,
        }

    @staticmethod
    def from_model(delivery_station: CfgDeliveryStation) -> dict:
        return (
            DeliveryStationDTO(delivery_station).to_dict()
            if delivery_station
            else {}
        )

    @staticmethod
    def from_model_list(
        delivery_stations: List[CfgDeliveryStation],
    ) -> list[dict]:
        return [
            DeliveryStationDTO(delivery_station).to_dict()
            for delivery_station in delivery_stations
        ]
