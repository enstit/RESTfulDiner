# app/dto/printer.py


from typing import List

from app.config import Config
from app.models.printer import Printer


class PrinterDTO:
    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "name": "schema:name",
            "mac_address": "schema:macAddress",
            "ip_address": "schema:ipAddress",
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, printer: Printer):
        self.event_id = str(printer.event_id)
        self.printer_id = str(printer.printer_id)
        self.name = printer.name
        self.mac_address = printer.mac_address
        self.ip_address = str(printer.ip_address)

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/printers/{self.printer_id}",
            "type": "Printer",
            "name": self.name,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
        }

    @staticmethod
    def from_model(printer: Printer) -> dict:
        return {
            **PrinterDTO.CONTEXT,
            "data": PrinterDTO(printer).to_dict() if printer else None,
        }

    @staticmethod
    def from_model_list(printers: List[Printer]) -> dict:
        return {
            **PrinterDTO.CONTEXT,
            "data": [PrinterDTO(printer).to_dict() for printer in printers],
        }
