# app/dto/printer.py

from typing import List

from app.models.printer import Printer


class PrinterDTO:
    def __init__(self, printer: Printer):
        self.id = str(printer.id)
        self.name = printer.name
        self.mac_address = printer.mac_address
        self.ip_address = str(printer.ip_address)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
        }

    @staticmethod
    def from_model(printer: Printer) -> dict:
        return PrinterDTO(printer).to_dict() if printer else None

    @staticmethod
    def from_model_list(printers: List[Printer]) -> list:
        return [PrinterDTO(printer).to_dict() for printer in printers]
