# app/resources/printer.py

from flask_restful import Resource
from flask_restful import reqparse

from app.database import db
from app.dto.printer import PrinterDTO
from app.models.printer import Printer


class PrinterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name of the printer"
    )
    parser.add_argument(
        "mac_address",
        type=str,
        required=True,
        help="MAC address of the printer",
    )
    parser.add_argument(
        "ip_address",
        type=str,
        required=True,
        help="IP address of the printer",
    )

    def get(self, *, id: str | None = None, name: str | None = None):
        if id or name:
            printer = (
                db.session.query(Printer)
                .where(Printer.id == id if id else Printer.name == name)
                .one_or_none()
            )
            if printer:
                return PrinterDTO.from_model(printer), 200
            return {"message": f"Printer {name} was not found"}, 404
        printers = db.session.query(Printer).all()
        return PrinterDTO.from_model_list(printers), 200

    def post(self):
        data = PrinterResource.parser.parse_args()
        new_printer = Printer(
            name=data["name"],
            mac_address=data["mac_address"],
            ip_address=data["ip_address"],
        )
        db.session.add(new_printer)
        db.session.commit()
        return PrinterDTO.from_model(new_printer), 201
