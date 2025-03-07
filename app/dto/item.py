# app/dto/item.py

from typing import List

from app.config import Config
from app.models.item import Item


class ItemDTO:
    def __init__(self, item: Item):
        self.id = item.id
        self.name = item.name
        self.description = item.description
        self.department = item.department
        self.menu_section = item.menu_section
        self.price = item.price
        self.deposit = item.deposit
        self.availability = item.availability
        self.initial_status = item.initial_status

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/items/{self.id}",
            "name": self.name,
            "description": self.description,
            "department": (
                f"{Config.APP_URL}{Config.API_URI}/departments/{self.id}"
                if self.department
                else None
            ),
            "menu_section": self.menu_section.name,
            "price": self.price,
            "deposit": self.deposit,
            "availability": self.availability,
            "initial_status": self.initial_status.name,
        }

    @staticmethod
    def from_model(item: Item) -> dict:
        return ItemDTO(item).to_dict() if item else None

    @staticmethod
    def from_model_list(items: List[Item]) -> list:
        return [ItemDTO(item).to_dict() for item in items]
