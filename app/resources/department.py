# app/resources/department.py

from flask_restful import reqparse

from app.dto.department import DepartmentDTO
from app.extensions import db
from app.models.department import Department
from app.resources.auth import ProtectedResource


class DepartmentResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Name of the department"
    )

    def get(self, *, _id: str | None = None, name: str | None = None):
        if _id or name:
            department = (
                db.session.query(Department)
                .where(
                    Department.id == _id if _id else Department.name == name
                )
                .one_or_none()
            )
            if department:
                return DepartmentDTO.from_model(department), 200
            return {"message": f"Department {name} was not found"}, 404

        departments = db.session.query(Department).all()
        return DepartmentDTO.from_model_list(departments), 200

    def post(self):
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = DepartmentResource.parser.parse_args()
        new_department = Department(name=data["name"])
        db.session.add(new_department)
        db.session.commit()
        return DepartmentDTO.from_model(new_department), 201
