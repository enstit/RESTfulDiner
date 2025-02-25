# app/dto/department.py

from typing import List
from app.models.department import Department


class DepartmentDTO:
    def __init__(self, department: Department):
        self.id = str(department.id)
        self.name = department.name

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @staticmethod
    def from_model(department: Department) -> dict:
        return DepartmentDTO(department).to_dict() if department else None

    @staticmethod
    def from_model_list(departments: List[Department]) -> list:
        return [
            DepartmentDTO(department).to_dict() for department in departments
        ]
