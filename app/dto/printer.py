# app/dto/printer.py

from typing import List

from app.models.printer import Printer


class PrinterDTO:
    def __init__(self, printer: Printer):
        self.name = printer.name
        self.ip_address = printer.ip_address
        self.url = printer.url

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "ip_address": self.ip_address,
            "url": self.url,
        }

    @staticmethod
    def from_model(printer: Printer) -> dict:
        return PrinterDTO(printer).to_dict() if printer else None

    @staticmethod
    def from_model_list(printers: List[Printer]) -> list:
        return [PrinterDTO(printer).to_dict() for printer in printers]
