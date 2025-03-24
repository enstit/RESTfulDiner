# app/resources/printer.py

from flask_restful import reqparse

from app.dto.printer import PrinterDTO
from app.extensions import db
from app.models.printer import Printer
from app.resources.auth import ProtectedResource


class PrinterResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("mac_address", type=str)
    parser.add_argument("ip_address", type=str)

    def get(
        self, *, _id: str | None = None, name: str | None = None
    ) -> tuple[dict, int]:
        if _id or name:
            printer = (
                db.session.query(Printer)
                .where(Printer.id == _id if _id else Printer.name == name)
                .one_or_none()
            )
            if printer:
                return PrinterDTO.from_model(printer), 200
            return {"message": "Printer was not found"}, 404
        printers = db.session.query(Printer).all()
        return PrinterDTO.from_model_list(printers), 200

    def post(self):
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = PrinterResource.parser.parse_args()
        new_printer = Printer(
            name=data["name"],
            mac_address=data["mac_address"],
            ip_address=data["ip_address"],
        )
        db.session.add(new_printer)
        db.session.commit()
        return PrinterDTO.from_model(new_printer), 201
