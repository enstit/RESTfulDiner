# app/dto/item.py

from typing import List

from app.models.item import Item


class ItemDTO:
    def __init__(self, item: Item):
        self.name = item.name
        self.description = item.description
        self.department = item.department
        self.menu_section = item.menu_section
        self.price = item.price
        self.deposit = item.deposit
        self.availability = item.availability
        self.initial_status = item.initial_status
        self.url = item.url

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "department": self.department.name,
            "menu_section": self.menu_section.name,
            "price": self.price,
            "deposit": self.deposit,
            "availability": self.availability,
            "initial_status": self.initial_status.name,
            "url": self.url,
        }

    @staticmethod
    def from_model(item: Item) -> dict:
        return ItemDTO(item).to_dict() if item else None

    @staticmethod
    def from_model_list(items: List[Item]) -> list:
        return [ItemDTO(item).to_dict() for item in items]
