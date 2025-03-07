# app/dto/kiosk.py

from typing import List

from app.config import Config
from app.models.delivery_station import DeliveryStation


class DeliveryStationDTO:

    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "name": "schema:name",
            "is_active": "schema:publicAccess",
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, delivery_station: DeliveryStation):
        self.id = str(delivery_station.id)
        self.name = delivery_station.name
        self.is_active = delivery_station.active_flag

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/delivery_stations/{self.id}",
            "type": "schema:Place",
            "name": self.name,
            "is_active": self.is_active,
        }

    @staticmethod
    def from_model(delivery_station: DeliveryStation) -> dict:
        return (
            {
                **DeliveryStationDTO.CONTEXT,
                "data": DeliveryStationDTO(delivery_station).to_dict(),
            }
            if delivery_station
            else None
        )

    @staticmethod
    def from_model_list(delivery_stations: List[DeliveryStation]) -> dict:
        return {
            **DeliveryStationDTO.CONTEXT,
            "data": [
                DeliveryStationDTO(delivery_station).to_dict()
                for delivery_station in delivery_stations
            ],
        }
