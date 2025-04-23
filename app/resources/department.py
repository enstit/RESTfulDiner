# app/resources/department.py

from flask_restful import reqparse

from app.dto.department import DepartmentDTO
from app.extensions import db
from app.models.department import Department
from app.models.printer import Printer
from app.resources.auth import ProtectedResource


class DepartmentResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("printer_id", type=str)

    def get(
        self, *, _id: str | None = None, name: str | None = None
    ) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if _id or name:
            department = (
                db.session.query(Department)
                .where(Department.event_id == msg.get("event_id"))
                .where(
                    Department.department_id == _id
                    if _id
                    else Department.name == name
                )
                .one_or_none()
            )
            if department:
                return DepartmentDTO.from_model(department), 200
            return {"message": "Department was not found"}, 404

        departments = db.session.query(Department).all()
        return DepartmentDTO.from_model_list(departments), 200

    def post(self) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        new_department = Department(
            event__id=msg.get("event_id"), name=data["name"]
        )
        db.session.add(new_department)
        db.session.commit()
        return DepartmentDTO.from_model(new_department), 201

    def put(self, _id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        department = (
            db.session.query(Department)
            .where(Department.event_id == msg.get("event_id"))
            .where(Department.department_id == _id)
            .one_or_none()
        )
        if not department:
            return {"message": f"Department {_id} was not found"}, 404
        department.name = data["name"]
        printer = (
            db.session.query(Printer)
            .where(Printer.printer_id == data["printer_id"])
            .one_or_none()
        )
        department.printer = printer if printer else None

        db.session.commit()
        return DepartmentDTO.from_model(department), 200

    def patch(self, _id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        department = (
            db.session.query(Department)
            .where(Department.event_id == msg.get("event_id"))
            .where(Department.department_id == _id)
            .one_or_none()
        )
        if not department:
            return {"message": f"Department {_id} was not found"}, 404
        if "name" in data and data["name"]:
            department.name = data["name"]
        if "printer_id" in data and data["printer_id"]:
            printer = (
                db.session.query(Printer)
                .where(Printer.printer_id == data["printer_id"])
                .one_or_none()
            )
            if not printer:
                return {"message": "Printer not found"}, 404
            department.printer = printer

        db.session.commit()
        return DepartmentDTO.from_model(department), 200
