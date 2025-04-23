# app/dto/kiosk.py


from typing import List

from app.config import Config
from app.models.cfg_kiosk import CfgKiosk


class KioskDTO:
    def __init__(self, kiosk: CfgKiosk):
        self.event_id = str(kiosk.event_id)
        self.kiosk_id = str(kiosk.kiosk_id)
        self.name = kiosk.name
        self.printer_id = str(kiosk.printer_id) if kiosk.printer else None

    def to_dict(self) -> dict:
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/kiosks/{self.kiosk_id}",
            "id": self.kiosk_id,
            "name": self.name,
            "printer_url": (
                f"{Config.APP_URL}{Config.API_URI}/printers/{self.printer_id}"
                if self.printer_id
                else None
            ),
        }

    @staticmethod
    def from_model(kiosk: CfgKiosk) -> dict:
        return KioskDTO(kiosk).to_dict() if kiosk else {}

    @staticmethod
    def from_model_list(kiosks: List[CfgKiosk]) -> list[dict]:
        return [KioskDTO(kiosk).to_dict() for kiosk in kiosks]
