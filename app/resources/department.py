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
        self, *, department_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if department_id:
            department = (
                db.session.query(Department)
                .filter(
                    Department.event_id == msg.get("event_id"),
                    Department.department_id == department_id,
                )
                .one_or_none()
            )
            if department:
                return DepartmentDTO.from_model(department), 200
            return {"message": "Department was not found"}, 404

        departments = (
            db.session.query(Department)
            .filter(Department.event_id == msg.get("event_id"))
            .all()
        )
        return DepartmentDTO.from_model_list(departments), 200

    def post(self) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        new_department = Department(
            event_id=msg.get("event_id"), name=data["name"]
        )
        db.session.add(new_department)
        db.session.commit()
        return DepartmentDTO.from_model(new_department), 201

    def put(self, department_id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        new_name = data.get("name")
        new_printer_id = data.get("printer_id")

        department = (
            db.session.query(Department)
            .filter(
                Department.event_id == msg.get("event_id"),
                Department.department_id == department_id,
            )
            .one_or_none()
        )
        if not department:
            return {
                "message": f"Department {department_id} was not found"
            }, 404
        if new_name:
            department.name = new_name
        if new_printer_id:
            if not (
                printer := (
                    db.session.query(Printer)
                    .filter(
                        Printer.event_id == msg.get("event_id"),
                        Printer.printer_id == new_printer_id,
                    )
                    .one_or_none()
                )
            ):
                return {"message": f"Printer {new_printer_id} not found"}, 404
            department.printer = printer if printer else None
        db.session.commit()
        return DepartmentDTO.from_model(department), 200

    def patch(self, department_id: str) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        department = (
            db.session.query(Department)
            .filter(
                Department.event_id == msg.get("event_id"),
                Department.department_id == department_id,
            )
            .one_or_none()
        )
        if not department:
            return {
                "message": f"Department {department_id} was not found"
            }, 404
        if "name" in data and data["name"]:
            department.name = data["name"]
        if "printer_id" in data and data["printer_id"]:
            printer = (
                db.session.query(Printer)
                .filter(
                    Printer.event_id == msg.get("event_id"),
                    Printer.printer_id == data["printer_id"],
                )
                .one_or_none()
            )
            if not printer:
                return {"message": "Printer not found"}, 404
            department.printer = printer

        db.session.commit()
        return DepartmentDTO.from_model(department), 200
