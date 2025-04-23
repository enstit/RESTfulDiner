# app/dto/printer.py


from typing import List

from app.config import Config
from app.models.printer import Printer


class PrinterDTO:
    def __init__(self, printer: Printer):
        self.event_id = str(printer.event_id)
        self.printer_id = str(printer.printer_id)
        self.name = printer.name
        self.mac_address = printer.mac_address
        self.ip_address = str(printer.ip_address)

    def to_dict(self) -> dict:
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/printers/{self.printer_id}",
            "id": self.printer_id,
            "name": self.name,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
        }

    @staticmethod
    def from_model(printer: Printer) -> dict:
        return PrinterDTO(printer).to_dict() if printer else {}

    @staticmethod
    def from_model_list(printers: List[Printer]) -> list[dict]:
        return [PrinterDTO(printer).to_dict() for printer in printers]
