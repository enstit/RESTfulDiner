# app/dto/department.py

from typing import List

from app.config import Config
from app.models.department import Department


class DepartmentDTO:
    def __init__(self, department: Department):
        self.id = str(department.id)
        self.name = department.name
        self.printer = department.printer if department.printer else None

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/departments/{self.id}",
            "name": self.name,
            "printer": (
                f"{Config.APP_URL}{Config.API_URI}/printers/{self.printer.id}"
                if self.printer
                else None
            ),
        }

    @staticmethod
    def from_model(department: Department) -> dict:
        return DepartmentDTO(department).to_dict() if department else None

    @staticmethod
    def from_model_list(departments: List[Department]) -> list:
        return [
            DepartmentDTO(department).to_dict() for department in departments
        ]
