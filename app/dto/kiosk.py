# app/dto/kiosk.py


from typing import List

from app.config import Config
from app.models.kiosk import Kiosk


class KioskDTO:

    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "name": "schema:name",
            "printer": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, kiosk: Kiosk):
        self.id = str(kiosk.id)
        self.name = kiosk.name
        self.printer = kiosk.printer if kiosk.printer else None

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/kiosks/{self.id}",
            "type": "schema:Place",
            "name": self.name,
            "printer": (
                f"{Config.APP_URL}{Config.API_URI}/printers/{self.printer.id}"
                if self.printer
                else None
            ),
        }

    @staticmethod
    def from_model(kiosk: Kiosk) -> dict:
        return {
            **KioskDTO.CONTEXT,
            "data": KioskDTO(kiosk).to_dict() if kiosk else None,
        }

    @staticmethod
    def from_model_list(kiosks: List[Kiosk]) -> dict:
        return {
            **KioskDTO.CONTEXT,
            "data": [KioskDTO(kiosk).to_dict() for kiosk in kiosks],
        }
