# app/dto/item.py


from typing import List

from app.config import Config
from app.models.cfg_item import CfgItem


class ItemDTO:
    def __init__(self, item: CfgItem):
        self.event_id = str(item.event_id)
        self.item_id = str(item.item_id)
        self.name = item.name
        self.description = item.description
        self.department_id = (
            str(item.department_id) if item.department else None
        )
        self.menu_section = item.menu_section
        self.price = item.price
        self.deposit = item.deposit
        self.availability = item.availability
        self.initial_status = item.initial_status

    def to_dict(self) -> dict:
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/items/{self.item_id}",
            "id": self.item_id,
            "name": self.name,
            "description": self.description,
            "department_url": (
                f"{Config.APP_URL}{Config.API_URI}/departments/{self.department_id}"
                if self.department_id
                else None
            ),
            "menu_section": self.menu_section.name,
            "price": round(self.price, 2),
            "deposit": round(self.deposit, 2) if self.deposit else None,
            "availability": self.availability,
            "initial_status": self.initial_status.name,
        }

    @staticmethod
    def from_model(item: CfgItem) -> dict:
        return ItemDTO(item).to_dict() if item else {}

    @staticmethod
    def from_model_list(items: List[CfgItem]) -> list[dict]:
        return [ItemDTO(item).to_dict() for item in items]
