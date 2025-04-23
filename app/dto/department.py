# app/dto/department.py


from typing import List

from app.config import Config
from app.models.cfg_department import CfgDepartment


class DepartmentDTO:
    def __init__(self, department: CfgDepartment):
        self.event_id = str(department.event_id)
        self.department_id = str(department.department_id)
        self.name = department.name
        self.printer_id = (
            str(department.printer_id) if department.printer else None
        )

    def to_dict(self) -> dict:
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/departments/{self.department_id}",
            "id": self.department_id,
            "name": self.name,
            "printer_url": (
                f"{Config.APP_URL}{Config.API_URI}/printers/{self.printer_id}"
                if self.printer_id
                else None
            ),
        }

    @staticmethod
    def from_model(department: CfgDepartment) -> dict:
        return DepartmentDTO(department).to_dict() if department else {}

    @staticmethod
    def from_model_list(departments: List[CfgDepartment]) -> list[dict]:
        return [
            DepartmentDTO(department).to_dict() for department in departments
        ]
