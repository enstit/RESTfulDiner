# app/resources/printer.py

from flask_restful import reqparse

from app.dto.printer import PrinterDTO
from app.extensions import db
from app.models.cfg_printer import CfgPrinter
from app.resources.auth import ProtectedResource


class PrinterResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("mac_address", type=str)
    parser.add_argument("ip_address", type=str)

    def get(
        self, *, printer_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if printer_id:
            printer = (
                db.session.query(CfgPrinter)
                .filter(
                    CfgPrinter.event_id == msg.get("event_id"),
                    CfgPrinter.printer_id == printer_id,
                )
                .one_or_none()
            )
            if printer:
                return PrinterDTO.from_model(printer), 200
            return {
                "error": f"Printer {printer_id} was not found in the current event"
            }, 404
        printers = (
            db.session.query(CfgPrinter)
            .filter(CfgPrinter.event_id == msg.get("event_id"))
            .all()
        )
        return PrinterDTO.from_model_list(printers), 200

    def post(self):
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = PrinterResource.parser.parse_args()
        new_printer = CfgPrinter(
            event_id=msg.get("event_id"),
            name=data["name"],
            mac_address=data["mac_address"],
            ip_address=data["ip_address"],
        )
        db.session.add(new_printer)
        db.session.commit()
        return PrinterDTO.from_model(new_printer), 201
